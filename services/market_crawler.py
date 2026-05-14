"""시장 스냅샷 크롤러 서비스 레이어.

두 크롤러의 공통 로직을 임포트 가능한 형태로 제공합니다.

- NaverMarketCrawler: finance.naver.com 시가총액 순위 (HTML 파싱)
- DaumMarketCrawler:  finance.daum.net JSON API (전체 상장 종목 + 외국인비율)

반환 타입은 모두 list[dict] (JSON 직렬화 가능) 이므로
Flask API → MongoDB 저장 → Django 대시보드 표시까지 변환 없이 사용됩니다.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse

import requests
from lxml import html

logger = logging.getLogger(__name__)

NAVER_MARKET_URL = "https://finance.naver.com/sise/sise_market_sum.naver"
DAUM_STOCKS_URL = "https://finance.daum.net/api/quotes/stocks"

_NAVER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Referer": "https://finance.naver.com/",
}

_DAUM_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://finance.daum.net/",
    "Accept": "application/json, text/plain, */*",
}


class NaverMarketCrawler:
    """Naver Finance 시가총액 순위 크롤러 (HTML 파싱).

    페이지당 50종목, market_cap(시가총액 억원) 포함.

    반환 dict 필드:
        code, name, market, current_price, change_rate,
        volume, market_cap, crawled_at
    """

    def __init__(self, delay: float = 0.5):
        self.session = requests.Session()
        self.session.headers.update(_NAVER_HEADERS)
        self.delay = delay

    def crawl(self, market: str = "KOSPI", pages: int = 1) -> list[dict]:
        """시가총액 순위 크롤링. pages × 50종목."""
        sosok = "0" if market.upper() == "KOSPI" else "1"
        result: list[dict] = []

        for page in range(1, pages + 1):
            url = f"{NAVER_MARKET_URL}?sosok={sosok}&page={page}"
            logger.info("Naver market page %d/%d: %s", page, pages, url)
            try:
                resp = self.session.get(url, timeout=15)
                resp.raise_for_status()
            except requests.RequestException as exc:
                logger.warning("페이지 %d 실패: %s", page, exc)
                break

            items = self._parse_html(resp.text, market.upper())
            if not items:
                break
            result.extend(items)
            logger.info("  %d종목 수집 (누적 %d)", len(items), len(result))

            if page < pages:
                time.sleep(self.delay)

        logger.info("Naver 크롤링 완료: 총 %d종목", len(result))
        return result

    def _parse_html(self, html_text: str, market: str) -> list[dict]:
        now = datetime.now(timezone.utc).isoformat()
        items: list[dict] = []
        try:
            doc = html.fromstring(html_text)
        except Exception as exc:
            logger.warning("HTML 파싱 실패: %s", exc)
            return items

        for row in doc.xpath('//table[@class="type_2"]//tr'):
            link = row.xpath('.//a[contains(@href, "/item/main.naver")][1]')
            if not link:
                continue
            href = link[0].get("href", "")
            code = _extract_naver_code(href)
            name = link[0].text_content().strip()
            cells = [" ".join(td.xpath(".//text()")).strip() for td in row.xpath("./td")]
            if len(cells) < 10:
                continue
            items.append({
                "code": code,
                "name": name,
                "market": market,
                "current_price": _to_int(cells[2]),
                "change_rate": _to_float(cells[4]),
                "volume": _to_int(cells[9]),
                "market_cap": _to_int(cells[6]),
                "crawled_at": now,
            })
        return items


class DaumMarketCrawler:
    """Daum Finance JSON API 크롤러 (인증 불필요, Referer 헤더로 접근).

    KOSPI 약 2,444종목 / KOSDAQ 약 1,822종목을 단일 요청으로 수집.
    외국인보유비율(foreign_ratio), 누적거래대금(acc_trade_price) 포함.

    반환 dict 필드:
        symbol_code, name, market, trade_price, change, change_price,
        change_rate, acc_trade_volume, acc_trade_price, foreign_ratio, crawled_at
    """

    def __init__(self, delay: float = 0.3):
        self.session = requests.Session()
        self.session.headers.update(_DAUM_HEADERS)
        self.delay = delay

    def crawl(self, market: str = "KOSPI", per_page: int = 50, pages: int = 1) -> list[dict]:
        """전체 상장 종목 실시간 시세 수집.

        Daum API는 market= 지정 시 perPage와 무관하게 전체 종목을 반환합니다.
        """
        result: list[dict] = []
        for page in range(1, pages + 1):
            items = self._fetch_page(market.upper(), per_page, page)
            if not items:
                break
            result.extend(items)
            logger.info("  page %d: %d종목 (누적 %d)", page, len(items), len(result))
            if page < pages:
                time.sleep(self.delay)

        logger.info("Daum 크롤링 완료: 총 %d종목", len(result))
        return result

    def _fetch_page(self, market: str, per_page: int, page: int) -> list[dict]:
        params = {"market": market, "perPage": per_page, "page": page}
        logger.info("Daum API: market=%s page=%d", market, page)
        try:
            resp = self.session.get(DAUM_STOCKS_URL, params=params, timeout=15)
            resp.raise_for_status()
            payload = resp.json()
        except Exception as exc:
            logger.warning("Daum API 요청 실패: %s", exc)
            return []

        now = datetime.now(timezone.utc).isoformat()
        items: list[dict] = []
        for item in payload.get("data", []):
            trade_price = item.get("tradePrice")
            if trade_price is None:
                continue
            sym = item.get("symbolCode", "")
            items.append({
                "symbol_code": sym[1:] if sym.startswith("A") else sym,
                "name": item.get("name", ""),
                "market": market,
                "trade_price": int(trade_price),
                "change": _normalize_change(item.get("change", "")),
                "change_price": int(item.get("changePrice") or 0),
                "change_rate": round(float(item.get("changeRate") or 0) * 100, 4),
                "acc_trade_volume": int(item.get("accTradeVolume") or 0),
                "acc_trade_price": int(item.get("accTradePrice") or 0),
                "foreign_ratio": round(float(item.get("foreignRatio") or 0) * 100, 4),
                "crawled_at": now,
            })
        return items


def _extract_naver_code(href: str) -> str:
    q = parse_qs(urlparse(href).query)
    return q.get("code", [""])[0]


def _to_int(text: str) -> int:
    cleaned = text.replace(",", "").replace("원", "").replace("+", "").replace("-", "").strip()
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


def _normalize_change(change: str) -> str:
    return {"RISE": "상승", "FALL": "하락", "EVEN": "보합"}.get(change, change)
