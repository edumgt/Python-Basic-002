# finance.daum.net 크롤러

다음 금융 JSON API(`finance.daum.net/api/quotes/stocks`)에서 KOSPI/KOSDAQ 전체 종목의 실시간 시세와 외국인 보유비율을 수집합니다.

## 역할

이 크롤러는 **전체 상장 종목 실시간 스냅샷** 용도입니다.

- HTML 파싱 없이 JSON API를 직접 호출 (파싱 오류 위험 없음)
- KOSPI 2,444종목 / KOSDAQ 1,822종목 전체를 단일 요청으로 수집
- **외국인 보유비율(`foreign_ratio`)** 포함 — Naver 크롤러에 없는 ML 특징 변수
- 거래대금(`acc_trade_price`) 포함 — 유동성 필터링에 활용

> Naver 크롤러(`finance.naver.com/crawler.py`)는 시가총액 순위 상위 종목(HTML 파싱),  
> Daum 크롤러는 전체 상장 종목 실시간 시세(JSON API)를 수집합니다. 두 크롤러는 상호 보완적입니다.

## 수집 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| `symbol_code` | str | 종목 코드 (6자리 또는 ETF 코드) |
| `name` | str | 종목명 |
| `market` | str | 시장 구분 (`KOSPI`/`KOSDAQ`) |
| `trade_price` | int | 현재가 (원) |
| `change` | str | 등락 방향 (`상승`/`하락`/`보합`) |
| `change_price` | int | 전일대비 가격 변동 (원) |
| `change_rate` | float | 전일대비 등락률 (%) |
| `acc_trade_volume` | int | 누적 거래량 |
| `acc_trade_price` | int | 누적 거래대금 (원) |
| `foreign_ratio` | float | 외국인 보유비율 (%) |
| `crawled_at` | str | 수집 시각 (ISO 8601, UTC) |

## 실행

```bash
# KOSPI 전체 (기본: 50종목 단위 1페이지 요청, API는 전체 반환)
python finance.daum.net/crawler.py --market KOSPI --per-page 50 --pages 1

# KOSDAQ, JSON만 저장
python finance.daum.net/crawler.py --market KOSDAQ --output-format json --output-dir ./out
```

## 실제 실행 결과

- **실행 일시 (UTC)**: `2026-05-14T06:53:02Z`
- **실행 환경**: WSL2 (Linux 6.6, Python 3.12)
- **실행 명령**:

```bash
python finance.daum.net/crawler.py --market KOSPI --per-page 50 --pages 1 --output-format json --output-dir /tmp/daum_out
python finance.daum.net/crawler.py --market KOSDAQ --per-page 50 --pages 1 --output-format json --output-dir /tmp/daum_out
```

### KOSPI 결과

```
2026-05-14 15:53:01 [INFO] 크롤링 시작: market=KOSPI, pages=1, per_page=50
2026-05-14 15:53:01 [INFO]   요청: https://finance.daum.net/api/quotes/stocks?market=KOSPI&perPage=50&page=1
2026-05-14 15:53:02 [INFO]   페이지 1/1: 2444개 수집 (누적 2444개)
2026-05-14 15:53:02 [INFO] 크롤링 완료: 총 2444개 종목 수집
```

> Daum API는 `market=KOSPI` 지정 시 `perPage` 파라미터와 무관하게 전체 종목을 반환합니다.

주요 종목 샘플:

| 종목코드 | 종목명 | 현재가 | 등락 | 등락률 | 외국인비율 |
|---|---|---|---|---|---|
| 005930 | 삼성전자 | 296,000 | 상승 | +4.23% | 48.83% |
| 000660 | SK하이닉스 | 1,970,000 | 하락 | -0.30% | 52.37% |
| 005935 | 삼성전자우 | 193,700 | 상승 | +2.43% | 77.10% |
| 035420 | NAVER | 213,000 | 상승 | +5.71% | 36.82% |
| 000270 | 기아 | 178,100 | 하락 | -0.78% | 38.48% |

JSON 샘플 (삼성전자):

```json
{
  "symbol_code": "005930",
  "name": "삼성전자",
  "market": "KOSPI",
  "trade_price": 296000,
  "change": "상승",
  "change_price": 12000,
  "change_rate": 4.2254,
  "acc_trade_volume": 39278728,
  "acc_trade_price": 11521630256750,
  "foreign_ratio": 48.827,
  "crawled_at": "2026-05-14T06:53:02.096266+00:00"
}
```

### KOSDAQ 결과

```
2026-05-14 15:53:39 [INFO] 크롤링 시작: market=KOSDAQ, pages=1, per_page=50
2026-05-14 15:53:39 [INFO]   요청: https://finance.daum.net/api/quotes/stocks?market=KOSDAQ&perPage=50&page=1
2026-05-14 15:53:40 [INFO]   페이지 1/1: 1822개 수집 (누적 1822개)
2026-05-14 15:53:40 [INFO] 크롤링 완료: 총 1822개 종목 수집
```

거래대금 상위 종목 샘플:

| 종목코드 | 종목명 | 현재가 | 등락 | 등락률 | 외국인비율 |
|---|---|---|---|---|---|
| 080220 | 제주반도체 | 75,600 | 상승 | +28.35% | 7.47% |
| 010170 | 대한광통신 | 24,750 | 보합 | 0.00% | 4.64% |
| 100790 | 미래에셋벤처투자 | 59,900 | 상승 | +3.99% | 1.62% |

## Naver 크롤러와 비교

| 항목 | Naver (`finance.naver.com`) | Daum (`finance.daum.net`) |
|---|---|---|
| 수집 방식 | HTML 파싱 | JSON API |
| 수집 범위 | 시가총액 순위 상위 N종목 | 전체 상장 종목 |
| 시가총액 | ✅ 포함 | ❌ 없음 |
| 외국인비율 | ❌ 없음 | ✅ 포함 |
| 거래대금 | ❌ 없음 | ✅ 포함 |
| 속도 (1회) | ~0.2초 (HTML fetch) | ~0.3초 (JSON fetch) |

## 출력 형식

`--output-format` 옵션으로 JSON / XML / both 선택:

```
stocks_kospi_20260514_155302.json
stocks_kospi_20260514_155302.xml
```

JSON 루트 구조:

```json
{
  "source": "finance.daum.net",
  "crawled_at": "...",
  "total_count": 2444,
  "stocks": [...]
}
```
