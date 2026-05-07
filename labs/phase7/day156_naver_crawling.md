# Day 156 – 네이버 주식 페이지 크롤링 데이터 수집

> **소요시간**: 8시간 | **Phase**: 7 확장 – 프로젝트 데이터 파이프라인

---

## 🎯 학습 목표

- 네이버 금융 페이지에서 종목/지표 데이터 수집
- `requests + BeautifulSoup` 기반 크롤러 구현
- 수집 데이터 정제 후 CSV/SQLite 저장
- 수집 데이터를 군집화·예측 모델 입력으로 연결

---

## 📖 이론 (08:00 – 10:00)

- 크롤링 윤리: robots.txt, 요청 간격, 재시도 정책
- HTML 파싱 안정화: 선택자 버전 관리
- 스키마 표준화: 종목코드·날짜·가격·거래량

---

## 🧪 LAB 1 – 네이버 시세 크롤러 (10:00 – 12:00)

```python
import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/item/sise_day.naver?code=005930&page=1"
resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
soup = BeautifulSoup(resp.text, "lxml")
rows = soup.select("table.type2 tr")
```

---

## 🧪 LAB 2 – 데이터 정제 및 저장 (13:00 – 15:00)

- 숫자 포맷(콤마/부호) 정리
- 결측 행 제거
- CSV + SQLite 동시 저장

---

## 🧪 LAB 3 – 품질 점검 & 재실행 파이프라인 (15:00 – 17:00)

- 중복 행 검출
- 실패 페이지 재수집
- 일별 자동 수집 스케줄러 등록

---

## ✅ 체크리스트

- [ ] 네이버 시세/기초정보 크롤링 성공
- [ ] 정제 후 파일/DB 저장 성공
- [ ] 모델 입력용 데이터셋 생성 완료
