"""
Daum Finance (finance.daum.net) Stock Information Crawler

다음 금융 주식 정보 크롤러.
현재 finance.daum.net API는 Kakao 인증이 필요하므로,
Naver Finance의 KOSDAQ/KOSPI 시가총액 페이지와
개별 종목 상세 API(api.finance.naver.com)를 병행하여 수집합니다.

Usage:
    python crawler.py [--market MARKET] [--max-pages MAX_PAGES] [--output-format FORMAT]

Examples:
    python crawler.py --market KOSDAQ --max-pages 2
    python crawler.py --market KOSPI --output-format json
"""

import argparse
import json
import logging
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import List, Optional
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

import requests
from lxml import html

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("finance.daum.crawler")

NAVER_BASE = "https://finance.naver.com"
NAVER_MARKET_URL = f"{NAVER_BASE}/sise/sise_market_sum.naver"
NAVER_ITEM_API = "https://api.finance.naver.com/service/itemSummary.nhn"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://finance.naver.com/",
}

REQUEST_DELAY = 0.5


@dataclass
class StockInfo:
    """주식 데이터 모델 (다음 금융 호환)"""

    symbol_code: str = ""
    name: str = ""
    market: str = ""
    current_price: int = 0
    change_rate: float = 0.0
    volume: int = 0
    market_cap: int = 0
    per: float = 0.0
    pbr: float = 0.0
    eps: int = 0
    foreign_ratio: float = 0.0
    crawled_at: str = ""


class DaumStockCrawler:
    """
    다음 금융 호환 주식 크롤러.
    Naver Finance 시가총액 페이지에서 종목 목록을 가져오고,
    api.finance.naver.com에서 PER/PBR/외국인비율 등 상세 지표를 보강합니다.
    """

    def __init__(self, delay: float = REQUEST_DELAY):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.delay = delay
        self.stocks: List[StockInfo] = []

    def crawl_market(self, market: str = "KOSDAQ", max_pages: int = 1) -> List[StockInfo]:
        """시장(KOSPI/KOSDAQ)의 주식 정보를 수집합니다."""
        market_map = {"KOSPI": "0", "KOSDAQ": "1"}
        sosok = market_map.get(market.upper(), "1")

        logger.info("크롤링 시작: market=%s, max_pages=%d", market.upper(), max_pages)
        all_stocks: List[StockInfo] = []

        for page in range(1, max_pages + 1):
            params = {"sosok": sosok, "page": page}
            url = f"{NAVER_MARKET_URL}?{urlencode(params)}"
            logger.info("  페이지 %d/%d 요청: %s", page, max_pages, url)

            try:
                resp = self.session.get(url, timeout=15)
                resp.raise_for_status()
            except requests.RequestException as exc:
                logger.warning("요청 실패 (page=%d): %s", page, exc)
                break

            items = self._extract_stocks_from_html(resp.text, market.upper())
            if not items:
                logger.info("  더 이상 종목이 없습니다. 크롤링 종료.")
                break

            # 개별 종목 상세 지표 보강
            items = self._enrich_with_detail(items)

            all_stocks.extend(items)
            logger.info("  %d개 종목 수집 (누적 %d개)", len(items), len(all_stocks))

            if page < max_pages:
                time.sleep(self.delay)

        self.stocks.extend(all_stocks)
        logger.info("크롤링 완료: 총 %d개 종목 수집", len(all_stocks))
        return all_stocks

    def _extract_stocks_from_html(self, html_text: str, market: str) -> List[StockInfo]:
        """시가총액 HTML 테이블에서 주식 정보를 추출합니다."""
        stocks: List[StockInfo] = []
        now = datetime.now(timezone.utc).isoformat()

        try:
            doc = html.fromstring(html_text)
        except Exception as exc:
            logger.warning("HTML 파싱 실패: %s", exc)
            return stocks

        rows = doc.xpath('//table[@class="type_2"]//tr')
        for row in rows:
            link = row.xpath('.//a[contains(@href, "/item/main.naver")][1]')
            if not link:
                continue

            href = link[0].get("href", "")
            code = _extract_code(href)
            name = link[0].text_content().strip()

            cells = [" ".join(td.xpath(".//text()")).strip() for td in row.xpath("./td")]
            if len(cells) < 10:
                continue

            stock = StockInfo(
                symbol_code=code,
                name=name,
                market=market,
                current_price=_to_int(cells[2]),
                change_rate=_to_float(cells[4].replace("+", "")),
                market_cap=_to_int(cells[6]),
                volume=_to_int(cells[9]),
                crawled_at=now,
            )
            stocks.append(stock)

        return stocks

    def _enrich_with_detail(self, stocks: List[StockInfo]) -> List[StockInfo]:
        """api.finance.naver.com에서 PER, PBR, EPS 등 지표를 보강합니다."""
        for stock in stocks:
            if not stock.symbol_code:
                continue
            try:
                resp = self.session.get(
                    NAVER_ITEM_API,
                    params={"itemcode": stock.symbol_code},
                    timeout=8,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    stock.per = _to_float(str(data.get("per", 0)))
                    stock.pbr = _to_float(str(data.get("pbr", 0)))
                    stock.eps = _to_int(str(data.get("eps", 0)))
                    stock.foreign_ratio = _to_float(str(data.get("quant", 0)))
            except Exception as exc:
                logger.debug("상세 지표 수집 실패 (%s): %s", stock.symbol_code, exc)
            time.sleep(self.delay)
        return stocks

    def export_json(self, filepath: str) -> None:
        """수집된 종목 데이터를 JSON 파일로 저장합니다."""
        data = {
            "source": "finance.daum.net (via naver finance api)",
            "crawled_at": datetime.now(timezone.utc).isoformat(),
            "total_count": len(self.stocks),
            "stocks": [asdict(s) for s in self.stocks],
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("JSON 저장 완료: %s (%d개 종목)", filepath, len(self.stocks))

    def export_xml(self, filepath: str) -> None:
        """수집된 종목 데이터를 XML 파일로 저장합니다."""
        root = ET.Element("DaumStockInfos")
        root.set("source", "finance.daum.net")
        root.set("crawledAt", datetime.now(timezone.utc).isoformat())
        root.set("totalCount", str(len(self.stocks)))

        for stock in self.stocks:
            el = ET.SubElement(root, "Stock")
            el.set("code", stock.symbol_code)
            _add_xml_element(el, "Name", stock.name)
            _add_xml_element(el, "Market", stock.market)
            _add_xml_element(el, "CurrentPrice", str(stock.current_price))
            _add_xml_element(el, "ChangeRate", str(stock.change_rate))
            _add_xml_element(el, "Volume", str(stock.volume))
            _add_xml_element(el, "MarketCap", str(stock.market_cap))
            _add_xml_element(el, "PER", str(stock.per))
            _add_xml_element(el, "PBR", str(stock.pbr))
            _add_xml_element(el, "EPS", str(stock.eps))
            _add_xml_element(el, "CrawledAt", stock.crawled_at)
            if stock.symbol_code:
                _add_xml_element(
                    el, "StockUrl",
                    urljoin(NAVER_BASE, f"/item/main.naver?code={stock.symbol_code}"),
                )

        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
        logger.info("XML 저장 완료: %s (%d개 종목)", filepath, len(self.stocks))


def _extract_code(href: str) -> str:
    parsed = urlparse(href)
    query = parse_qs(parsed.query)
    return query.get("code", [""])[0]


def _add_xml_element(parent: ET.Element, tag: str, text: str) -> ET.Element:
    el = ET.SubElement(parent, tag)
    el.text = text
    return el


def _to_int(text: str) -> int:
    cleaned = text.replace(",", "").replace("원", "").replace("%", "").strip()
    cleaned = cleaned.replace("+", "").replace("-", "")
    try:
        return int(float(cleaned))
    except ValueError:
        return 0


def _to_float(text: str) -> float:
    cleaned = text.replace(",", "").replace("%", "").replace("+", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def crawl(context) -> None:
    """zavod 프레임워크 호환 crawl 함수"""
    market = context.dataset.config.get("market", "KOSDAQ")
    max_pages = context.dataset.config.get("max_pages", 1)

    context.log.info(f"다음 금융 크롤링 시작: market={market}")

    crawler = DaumStockCrawler()
    stocks = crawler.crawl_market(market=market, max_pages=max_pages)

    for stock in stocks:
        context.log.info(
            f"종목: {stock.name}({stock.symbol_code}) | 현재가: {stock.current_price:,}원 | "
            f"PER: {stock.per} | PBR: {stock.pbr}"
        )

    context.log.info(f"크롤링 완료: 총 {len(stocks)}개 종목 수집")


def main():
    parser = argparse.ArgumentParser(
        description="다음 금융 호환 주식 정보 크롤러",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python crawler.py --market KOSDAQ --max-pages 2
  python crawler.py --market KOSPI --output-format json
        """,
    )
    parser.add_argument(
        "--market", type=str, choices=["KOSPI", "KOSDAQ"], default="KOSDAQ",
        help="수집할 시장 (기본값: KOSDAQ)",
    )
    parser.add_argument(
        "--max-pages", type=int, default=1,
        help="최대 크롤링 페이지 수 (기본값: 1)",
    )
    parser.add_argument(
        "--output-format", type=str, choices=["json", "xml", "both"], default="both",
        help="출력 형식 (기본값: both)",
    )
    parser.add_argument(
        "--output-dir", type=str, default=".",
        help="출력 디렉토리 (기본값: 현재 디렉토리)",
    )

    args = parser.parse_args()
    crawler = DaumStockCrawler()
    stocks = crawler.crawl_market(market=args.market, max_pages=args.max_pages)

    if not stocks:
        logger.warning("수집된 종목이 없습니다.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    market_name = args.market.lower()

    if args.output_format in ("json", "both"):
        crawler.export_json(f"{args.output_dir}/stocks_{market_name}_{timestamp}.json")
    if args.output_format in ("xml", "both"):
        crawler.export_xml(f"{args.output_dir}/stocks_{market_name}_{timestamp}.xml")

    logger.info("전체 작업 완료: %d개 종목 수집", len(stocks))


if __name__ == "__main__":
    main()
