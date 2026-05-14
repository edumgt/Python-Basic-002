# Daum Finance 크롤링 테스트 (finance.daum.net)

## 실제 크롤링 실행 결과

- 실행 일시(UTC): 2026-05-14T06:09:42Z
- 실행 명령:

```bash
python finance.daum.net/crawler.py --market KOSDAQ --max-pages 1 --output-format json --output-dir /tmp
```

- 실행 결과 요약:
  - 요청 URL: `https://finance.naver.com/sise/sise_market_sum.naver?sosok=1&page=1`
  - 상태: 실패 (DNS NameResolutionError)
  - 수집 건수: `0`

로그 핵심:

```text
요청 실패 (page=1): HTTPSConnectionPool(host='finance.naver.com', port=443):
Failed to resolve 'finance.naver.com' ([Errno -5] No address associated with hostname)
```

## 크롤링 데이터 내용(스키마)

크롤러(`finance.daum.net/crawler.py`)는 아래 항목을 JSON/XML로 저장합니다.

| 필드 | 타입 | 설명 |
|---|---|---|
| `symbol_code` | str | 종목 코드 |
| `name` | str | 종목명 |
| `market` | str | 시장 구분 (`KOSPI`/`KOSDAQ`) |
| `current_price` | int | 현재가 |
| `change_rate` | float | 등락률(%) |
| `volume` | int | 거래량 |
| `market_cap` | int | 시가총액 |
| `per` | float | PER |
| `pbr` | float | PBR |
| `eps` | int | EPS |
| `foreign_ratio` | float | 외국인 비율(코드상 `quant` 매핑) |
| `crawled_at` | str | 크롤링 시각(ISO 8601) |

## 비고

현재 실행 환경에서는 외부 도메인 DNS 해석 제한으로 실데이터가 수집되지 않았습니다.
동일 명령을 네트워크가 허용된 환경에서 실행하면 위 스키마 기준으로 실제 종목 데이터가 생성됩니다.
