"""
Daum Finance (finance.daum.net) Stock Information Crawler

다음 금융 JSON API에서 주식 정보를 수집합니다.
API: https://finance.daum.net/api/quotes/stocks?market=KOSPI&perPage=50&page=1

Naver Finance 크롤러(finance.naver.com/crawler.py)와 달리, Daum API는
JSON을 직접 반환하므로 HTML 파싱 없이 현재가·등락·외국인비율을 수집할 수 있습니다.

Usage:
    python crawler.py [--market MARKET] [--pages PAGES] [--per-page PER_PAGE]
                      [--output-format FORMAT] [--output-dir DIR]

Examples:
    python crawler.py --market KOSPI --per-page 50 --pages 1
    python crawler.py --market KOSDAQ --output-format json
    python crawler.py --market KOSPI --per-page 100 --pages 2 --output-dir ./out
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

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("finance.daum.crawler")

DAUM_API_BASE = "https://finance.daum.net/api/quotes/stocks"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://finance.daum.net/",
    "Accept": "application/json, text/plain, */*",
}

REQUEST_DELAY = 0.5


@dataclass
class StockInfo:
    """다음 금융 API 주식 데이터 모델"""

    symbol_code: str = ""
    name: str = ""
    market: str = ""
    trade_price: int = 0
    change: str = ""
    change_price: int = 0
    change_rate: float = 0.0
    acc_trade_volume: int = 0
    acc_trade_price: int = 0
    foreign_ratio: float = 0.0
    crawled_at: str = ""


class DaumStockCrawler:
    """
    다음 금융 JSON API 크롤러.

    Daum Finance API는 별도 인증 없이 Referer 헤더만으로 JSON 응답을 반환합니다.
    Naver Finance 크롤러(HTML 파싱)와 달리 정형화된 JSON을 직접 파싱하므로
    파싱 오류 위험이 낮고 외국인비율(foreign_ratio) 등 추가 지표를 포함합니다.
    """

    def __init__(self, delay: float = REQUEST_DELAY):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.delay = delay
        self.stocks: List[StockInfo] = []

    def crawl_market(
        self, market: str = "KOSPI", pages: int = 1, per_page: int = 50
    ) -> List[StockInfo]:
        """시장(KOSPI/KOSDAQ)의 주식 정보를 페이지 단위로 수집합니다."""
        logger.info(
            "크롤링 시작: market=%s, pages=%d, per_page=%d",
            market.upper(), pages, per_page,
        )
        all_stocks: List[StockInfo] = []

        for page in range(1, pages + 1):
            items = self._fetch_page(market.upper(), page, per_page)
            if not items:
                logger.info("  데이터 없음 – 크롤링 종료 (page=%d)", page)
                break

            all_stocks.extend(items)
            logger.info(
                "  페이지 %d/%d: %d개 수집 (누적 %d개)",
                page, pages, len(items), len(all_stocks),
            )

            if page < pages:
                time.sleep(self.delay)

        self.stocks.extend(all_stocks)
        logger.info("크롤링 완료: 총 %d개 종목 수집", len(all_stocks))
        return all_stocks

    def _fetch_page(
        self, market: str, page: int, per_page: int
    ) -> List[StockInfo]:
        """Daum Finance API에서 단일 페이지를 요청하고 파싱합니다."""
        params = {"market": market, "perPage": per_page, "page": page}
        url = f"{DAUM_API_BASE}?market={market}&perPage={per_page}&page={page}"
        logger.info("  요청: %s", url)

        try:
            resp = self.session.get(DAUM_API_BASE, params=params, timeout=15)
            resp.raise_for_status()
            payload = resp.json()
        except requests.RequestException as exc:
            logger.warning("요청 실패 (page=%d): %s", page, exc)
            return []
        except ValueError as exc:
            logger.warning("JSON 파싱 실패 (page=%d): %s", page, exc)
            return []

        raw_items = payload.get("data", [])
        if not raw_items:
            return []

        now = datetime.now(timezone.utc).isoformat()
        stocks: List[StockInfo] = []
        for item in raw_items:
            symbol_code = item.get("symbolCode", "")
            if symbol_code.startswith("A"):
                symbol_code = symbol_code[1:]

            trade_price = item.get("tradePrice")
            if trade_price is None:
                continue

            stocks.append(StockInfo(
                symbol_code=symbol_code,
                name=item.get("name", ""),
                market=market,
                trade_price=int(trade_price),
                change=_normalize_change(item.get("change", "")),
                change_price=int(item.get("changePrice") or 0),
                change_rate=round(float(item.get("changeRate") or 0) * 100, 4),
                acc_trade_volume=int(item.get("accTradeVolume") or 0),
                acc_trade_price=int(item.get("accTradePrice") or 0),
                foreign_ratio=round(float(item.get("foreignRatio") or 0) * 100, 4),
                crawled_at=now,
            ))

        return stocks

    def export_json(self, filepath: str) -> None:
        """수집된 종목 데이터를 JSON 파일로 저장합니다."""
        data = {
            "source": "finance.daum.net",
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
            _add_xml_element(el, "TradePrice", str(stock.trade_price))
            _add_xml_element(el, "Change", stock.change)
            _add_xml_element(el, "ChangePrice", str(stock.change_price))
            _add_xml_element(el, "ChangeRate", str(stock.change_rate))
            _add_xml_element(el, "AccTradeVolume", str(stock.acc_trade_volume))
            _add_xml_element(el, "AccTradePrice", str(stock.acc_trade_price))
            _add_xml_element(el, "ForeignRatio", str(stock.foreign_ratio))
            _add_xml_element(el, "CrawledAt", stock.crawled_at)

        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
        logger.info("XML 저장 완료: %s (%d개 종목)", filepath, len(self.stocks))


def _normalize_change(change: str) -> str:
    mapping = {"RISE": "상승", "FALL": "하락", "EVEN": "보합"}
    return mapping.get(change, change)


def _add_xml_element(parent: ET.Element, tag: str, text: str) -> ET.Element:
    el = ET.SubElement(parent, tag)
    el.text = text
    return el


def main():
    parser = argparse.ArgumentParser(
        description="다음 금융 주식 정보 크롤러 (finance.daum.net JSON API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python crawler.py --market KOSPI --per-page 50 --pages 1
  python crawler.py --market KOSDAQ --output-format json
  python crawler.py --market KOSPI --per-page 100 --pages 2
        """,
    )
    parser.add_argument(
        "--market", type=str, choices=["KOSPI", "KOSDAQ"], default="KOSPI",
        help="수집할 시장 (기본값: KOSPI)",
    )
    parser.add_argument(
        "--per-page", type=int, default=50,
        help="페이지당 종목 수 (기본값: 50, 최대 100)",
    )
    parser.add_argument(
        "--pages", type=int, default=1,
        help="수집할 페이지 수 (기본값: 1)",
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
    stocks = crawler.crawl_market(
        market=args.market, pages=args.pages, per_page=args.per_page
    )

    if not stocks:
        logger.warning("수집된 종목이 없습니다.")
        return

    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    market_name = args.market.lower()

    if args.output_format in ("json", "both"):
        crawler.export_json(f"{args.output_dir}/stocks_{market_name}_{timestamp}.json")
    if args.output_format in ("xml", "both"):
        crawler.export_xml(f"{args.output_dir}/stocks_{market_name}_{timestamp}.xml")

    logger.info("전체 작업 완료: %d개 종목 수집", len(stocks))


if __name__ == "__main__":
    main()
