# finance.naver.com 크롤러

네이버 금융 시가총액 순위 페이지(`sise_market_sum.naver`)를 HTML 파싱하여 KOSPI/KOSDAQ 상위 종목 정보를 수집합니다.

## 역할

이 크롤러는 **시가총액 순위 기반 종목 선정** 용도입니다.

- 시장(`KOSPI`/`KOSDAQ`)별 시가총액 순위 상위 종목 수집
- 페이지당 50종목, `--max-pages`로 수집 범위 조정
- 종목별 현재가·등락률·거래량·시가총액 제공
- ML 파이프라인에 투입할 유니버스(분석 대상 종목 목록) 구성에 활용

> 개별 종목 일별 OHLCV 수집은 `trading/naver_crawler.py`의 `NaverFinanceCrawler`를 사용합니다.

## 수집 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| `code` | str | 종목 코드 (6자리) |
| `name` | str | 종목명 |
| `market` | str | 시장 구분 (`KOSPI`/`KOSDAQ`) |
| `current_price` | int | 현재가 (원) |
| `change_rate` | float | 전일대비 등락률 (%) |
| `volume` | int | 거래량 |
| `market_cap` | int | 시가총액 (억 원) |
| `crawled_at` | str | 수집 시각 (ISO 8601, UTC) |

## 실행

```bash
# KOSPI 시가총액 상위 50종목 (1페이지)
python finance.naver.com/crawler.py --market KOSPI --max-pages 1

# KOSDAQ 2페이지 (100종목), JSON만 저장
python finance.naver.com/crawler.py --market KOSDAQ --max-pages 2 --output-format json --output-dir ./out
```

## 실제 실행 결과

- **실행 일시 (UTC)**: `2026-05-14T06:52:50Z`
- **실행 환경**: WSL2 (Linux 6.6, Python 3.12)
- **실행 명령**:

```bash
python finance.naver.com/crawler.py --market KOSPI --max-pages 1 --output-format json --output-dir /tmp/naver_out
python finance.naver.com/crawler.py --market KOSDAQ --max-pages 1 --output-format json --output-dir /tmp/naver_out
```

### KOSPI 결과

```
2026-05-14 15:52:50 [INFO] 주식 크롤링 시작: market=KOSPI, max_pages=1
2026-05-14 15:52:50 [INFO]   페이지 1/1 요청: https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page=1
2026-05-14 15:52:50 [INFO]   50개 종목 수집 (누적 50개)
2026-05-14 15:52:50 [INFO] 크롤링 완료: 총 50개 종목 수집
```

| 순위 | 종목코드 | 종목명 | 현재가 | 등락률 | 거래량 | 시가총액(억) |
|---|---|---|---|---|---|---|
| 1 | 005930 | 삼성전자 | 296,000 | +4.23% | 39,295,586 | 17,304,985 |
| 2 | 000660 | SK하이닉스 | 1,970,000 | -0.30% | 5,602,360 | 14,040,237 |
| 3 | 005935 | 삼성전자우 | 193,700 | +2.43% | 4,985,848 | 1,554,193 |
| 4 | 402340 | SK스퀘어 | 1,171,000 | -1.60% | 922,936 | 1,545,233 |
| 5 | 005380 | 현대차 | 712,000 | +0.28% | 2,399,570 | 1,457,875 |

JSON 샘플 (삼성전자):

```json
{
  "code": "005930",
  "name": "삼성전자",
  "market": "KOSPI",
  "current_price": 296000,
  "change_rate": 4.23,
  "volume": 39295586,
  "market_cap": 17304985,
  "crawled_at": "2026-05-14T06:52:50.860371+00:00"
}
```

### KOSDAQ 결과

```
2026-05-14 15:53:43 [INFO] 주식 크롤링 시작: market=KOSDAQ, max_pages=1
2026-05-14 15:53:43 [INFO]   50개 종목 수집 (누적 50개)
2026-05-14 15:53:43 [INFO] 크롤링 완료: 총 50개 종목 수집
```

| 순위 | 종목코드 | 종목명 | 현재가 | 등락률 | 거래량 | 시가총액(억) |
|---|---|---|---|---|---|---|
| 1 | 196170 | 알테오젠 | 385,000 | +8.76% | 1,116,899 | 206,105 |
| 2 | 247540 | 에코프로비엠 | 209,000 | +6.04% | 807,776 | 204,466 |
| 3 | 086520 | 에코프로 | 142,300 | +5.41% | 1,252,745 | 193,209 |

## 출력 형식

`--output-format` 옵션으로 JSON / XML / both 선택:

```
stocks_kospi_20260514_155250.json
stocks_kospi_20260514_155250.xml
```

JSON 루트 구조:

```json
{
  "crawled_at": "...",
  "total_count": 50,
  "stocks": [...]
}
```
