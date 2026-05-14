"""
Naver Finance (finance.naver.com) Stock Information Crawler

네이버 금융 시가총액 페이지에서 주식 정보를 수집하는 예시입니다.

Usage:
    python crawler.py [--market MARKET] [--max-pages MAX_PAGES] [--output-format FORMAT]

Examples:
    python crawler.py --market KOSPI --max-pages 2
    python crawler.py --market KOSDAQ --output-format json
"""

import argparse
import json
import logging
import os
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
logger = logging.getLogger("finance.naver.crawler")

BASE_URL = "https://finance.naver.com"
MARKET_SUM_URL = f"{BASE_URL}/sise/sise_market_sum.naver"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://finance.naver.com/",
}

REQUEST_DELAY = 1.0


@dataclass
class StockInfo:
    """네이버 금융 주식 데이터 모델"""

    code: str = ""
    name: str = ""
    market: str = ""
    current_price: int = 0
    change_rate: float = 0.0
    volume: int = 0
    market_cap: int = 0
    crawled_at: str = ""


class NaverStockCrawler:
    """네이버 금융 시가총액 페이지 크롤러"""

    def __init__(self, delay: float = REQUEST_DELAY):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.delay = delay
        self.stocks: List[StockInfo] = []

    def crawl_market(self, market: str = "KOSPI", max_pages: int = 1) -> List[StockInfo]:
        """시장(KOSPI/KOSDAQ)의 주식 정보를 수집합니다."""
        market_map = {"KOSPI": "0", "KOSDAQ": "1"}
        sosok = market_map.get(market.upper(), "0")

        logger.info("주식 크롤링 시작: market=%s, max_pages=%d", market.upper(), max_pages)
        all_stocks: List[StockInfo] = []

        for page in range(1, max_pages + 1):
            params = {"sosok": sosok, "page": page}
            url = f"{MARKET_SUM_URL}?{urlencode(params)}"
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
            stock_code = self._extract_stock_code(href)
            stock_name = link[0].text_content().strip()

            cells = [" ".join(td.xpath('.//text()')).strip() for td in row.xpath("./td")]
            if len(cells) < 10:
                continue

            stock = StockInfo(
                code=stock_code,
                name=stock_name,
                market=market,
                current_price=self._to_int(cells[2]),
                change_rate=self._to_float(cells[4]),
                market_cap=self._to_int(cells[6]),
                volume=self._to_int(cells[9]),
                crawled_at=now,
            )
            stocks.append(stock)

        return stocks

    def export_json(self, filepath: str) -> None:
        """수집된 종목 데이터를 JSON 파일로 저장합니다."""
        data = {
            "crawled_at": datetime.now(timezone.utc).isoformat(),
            "total_count": len(self.stocks),
            "stocks": [asdict(s) for s in self.stocks],
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("JSON 저장 완료: %s (%d개 종목)", filepath, len(self.stocks))

    def export_xml(self, filepath: str) -> None:
        """수집된 종목 데이터를 XML 파일로 저장합니다."""
        root = ET.Element("NaverStockInfos")
        root.set("crawledAt", datetime.now(timezone.utc).isoformat())
        root.set("totalCount", str(len(self.stocks)))

        for stock in self.stocks:
            stock_el = ET.SubElement(root, "Stock")
            stock_el.set("code", stock.code)

            _add_xml_element(stock_el, "Name", stock.name)
            _add_xml_element(stock_el, "Market", stock.market)
            _add_xml_element(stock_el, "CurrentPrice", str(stock.current_price))
            _add_xml_element(stock_el, "ChangeRate", str(stock.change_rate))
            _add_xml_element(stock_el, "Volume", str(stock.volume))
            _add_xml_element(stock_el, "MarketCap", str(stock.market_cap))
            _add_xml_element(stock_el, "CrawledAt", stock.crawled_at)
            if stock.code:
                _add_xml_element(stock_el, "StockUrl", urljoin(BASE_URL, f"/item/main.naver?code={stock.code}"))

        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
        logger.info("XML 저장 완료: %s (%d개 종목)", filepath, len(self.stocks))

    @staticmethod
    def _extract_stock_code(href: str) -> str:
        parsed = urlparse(href)
        query = parse_qs(parsed.query)
        return query.get("code", [""])[0]

    @staticmethod
    def _to_int(text: str) -> int:
        cleaned = text.replace(",", "").replace("원", "").replace("%", "").strip()
        cleaned = cleaned.replace("+", "").replace("-", "")
        try:
            return int(cleaned)
        except ValueError:
            return 0

    @staticmethod
    def _to_float(text: str) -> float:
        cleaned = text.replace(",", "").replace("%", "").replace("+", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0


def _add_xml_element(parent: ET.Element, tag: str, text: str) -> ET.Element:
    el = ET.SubElement(parent, tag)
    el.text = text
    return el


def main():
    parser = argparse.ArgumentParser(
        description="네이버 금융 주식 정보 크롤러",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python crawler.py --market KOSPI --max-pages 2
  python crawler.py --market KOSDAQ --output-format json
  python crawler.py --market KOSPI --output-format xml
        """,
    )
    parser.add_argument(
        "--market",
        type=str,
        choices=["KOSPI", "KOSDAQ"],
        default="KOSPI",
        help="수집할 시장 (기본값: KOSPI)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=1,
        help="최대 크롤링 페이지 수 (기본값: 1)",
    )
    parser.add_argument(
        "--output-format",
        type=str,
        choices=["json", "xml", "both"],
        default="both",
        help="출력 형식 (기본값: both)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="출력 디렉토리 (기본값: 현재 디렉토리)",
    )

    args = parser.parse_args()

    crawler = NaverStockCrawler()
    stocks = crawler.crawl_market(market=args.market, max_pages=args.max_pages)

    if not stocks:
        logger.warning("수집된 종목이 없습니다.")
        return

    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    market_name = args.market.lower()

    if args.output_format in ("json", "both"):
        json_path = f"{args.output_dir}/stocks_{market_name}_{timestamp}.json"
        crawler.export_json(json_path)

    if args.output_format in ("xml", "both"):
        xml_path = f"{args.output_dir}/stocks_{market_name}_{timestamp}.xml"
        crawler.export_xml(xml_path)

    logger.info("전체 작업 완료: %d개 종목 수집", len(stocks))


if __name__ == "__main__":
    main()
