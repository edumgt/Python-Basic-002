# 🐍 Python → FastAPI → 자동매매 AI 시스템 150일 LAB 커리큘럼

> **구성**: 하루 8시간 × 150일 = **1,200시간** 완성 로드맵  
> **스타일**: 매일 이론 강의(2h) + 실습 LAB(4h) + 과제 리뷰(2h)  
> **대상**: Python 입문자 → FastAPI 백엔드 개발자 → AI 자동매매 시스템 구축 완성

---

## 📋 전체 Phase 구조

> ⚡ **핵심 변경**: Python 기초 3단계를 **60일 → 30일로 압축**,  
> 확보된 30일을 **Phase 8 – 자동매매 시스템 실전**에 집중 투자

| Phase | 기간 | 일수 | 주제 | 핵심 기술 |
|-------|------|------|------|-----------|
| **Phase 1** | Day 01 – 10 | 10일 | Python 핵심 기초 **[압축]** | 문법·자료형·제어문·함수·컬렉션 |
| **Phase 2** | Day 11 – 20 | 10일 | 자료구조 & OOP **[압축]** | class·상속·dataclass·제너레이터 |
| **Phase 3** | Day 21 – 30 | 10일 | Python 고급 & 비동기 **[압축]** | 데코레이터·asyncio·Pydantic·pytest |
| **Phase 4** | Day 31 – 50 | 20일 | FastAPI 기초 | 라우팅·요청/응답·미들웨어·Swagger |
| **Phase 5** | Day 51 – 70 | 20일 | FastAPI 중급 | SQLite·SQLAlchemy·JWT·pytest |
| **Phase 6** | Day 71 – 90 | 20일 | FastAPI 고급 & 실전 | WebSocket·Docker·배포·최종 프로젝트 |
| **Phase 7** | Day 91 – 120 | 30일 | 금융 데이터 분석 & ML | yfinance·pandas·기술적분석·백테스트·LSTM |
| **Phase 8** | Day 121 – 150 | 30일 | **자동매매 시스템 실전** ✨ | Alpaca·키움증권·AI전략·리스크관리·EC2 운용 |

### 🧩 요청 커리큘럼 매핑 (충족/부분/미충족)

| 요청 영역 | 현재 상태 | 비고 |
|----------|----------|------|
| 퀀트를 위한 ML/DL (회귀·RF·LSTM 등) | **부분 충족** | 기존 Day 142~148 + 확장 Day 151~154 보강 |
| 투자분석 기초 방법론 (매크로·산업·밸류에이션) | **부분 충족** | 기존 Day 128 보유, DCF/FCF/EVA 확장 모듈 추가 |
| 퀀트를 위한 금융 필수 지식 (채권·파생·자산배분) | **부분 충족** | Phase 8 확장 Day 151~153에서 Risk-Parity/BL 보강 |
| 데이터 활용 퀀트 모델링 (성과지표·계절성·자동매매) | **부분 충족** | 기존 Day 136·137 + 확장 Day 155 보강 |
| 주가지수 데이터 활용 ML/DL 프로젝트 | **부분 충족** | 기존 Day 150 + 확장 Day 156(네이버 크롤링)·Day 154(군집화) |
| 로보어드바이저 개발 프로젝트 | **충족** | 기존 Phase 8 실전 자동매매/리스크/배포 구성 |
| 투자 인디케이터 개발 프로젝트 (PineScript) | **부분 충족** | 신규 Phase 9(Day 161~163) 트랙으로 보강 |

### 자동매매 기능 현황 (Phase 8 완료 후)

| 기능 | 상태 | 구현 모듈 |
|------|------|-----------|
| 자동매매 실행 | ✅ 완전 구현 | `trading/alpaca_client.py`, `trading/kiwoom_client.py` |
| AI 전략 실행 | ✅ 완전 구현 | `trading/ml_strategy.py` (RF·XGBoost·LSTM) |
| 증권사 연동 | ✅ 완전 구현 | Alpaca (미국) + 키움증권 (국내) |
| 리스크 관리 | ✅ 완전 구현 | `trading/risk_manager.py` (일손실·MDD·포지션 사이징) |
| 텔레그램 알림 | ✅ 완전 구현 | `trading/telegram_notifier.py` |
| 매매 기록 DB | ✅ 완전 구현 | `trading/trade_logger.py` (SQLite) |
| 서버 자동화 | ✅ 완전 구현 | systemd + CloudWatch + cron 백업 |

---

## 📅 Phase 1 – Python 핵심 기초 [10일 압축] (Day 01 ~ 10)

> 📌 **압축 방침**: 자동매매·데이터 분석에 직접 필요한 핵심 문법만 집중 학습.  
> 연산자·비트연산·튜플·정규표현식 등 심화 주제는 **선택 학습**으로 전환.  
> 참고 파일: `labs/phase1/` (Day 01–20 전체 보관, 필요 시 활용)

| Day | 압축 주제 (하루 2개 주제 병행) | 핵심 내용 | 심화 선택 파일 |
|-----|------|----------|----------------|
| 01 | 환경 구축 + 기본 자료형 | Python 설치, venv, int/float/str/bool, f-string | `day01_setup.md`, `day02_hello.md`, `day03_datatypes.md` |
| 02 | 조건문 + 반복문 | if/elif/else, for/while, break/continue, 삼항 | `day04_operators.md`, `day06_conditions.md`, `day07_loops.md` |
| 03 | 함수 기초 + 심화 | def/return, *args/**kwargs, 기본값, 스코프, lambda | `day08_functions.md`, `day09_advanced_functions.md` |
| 04 | 리스트 + 딕셔너리 | CRUD, 정렬, 컴프리헨션, .get(), 중첩 dict | `day10_list.md`, `day11_tuple.md`, `day12_dict.md` |
| 05 | 셋 + 파일 I/O | 집합 연산, open/read/write/with, CSV 읽기 | `day13_set.md`, `day14_fileio.md` |
| 06 | JSON + 예외처리 | json.dumps/loads, try/except/finally, 사용자 예외 | `day15_json.md`, `day16_exceptions.md` |
| 07 | 모듈 + 표준 라이브러리 | import, pip, os/sys/pathlib/datetime/collections | `day17_modules.md`, `day18_stdlib.md` |
| 08 | 문자열 + 포맷 | 슬라이싱, 메서드, format, 정규표현식 기초 | `day05_strings.md` |
| 09 | 미니 프로젝트 | 포트폴리오 수익률 계산기 (JSON 기반) | `day19_project_memo.md` |
| 10 | Phase 1 리뷰 | 코드 리뷰 + 취약점 보완 | `day20_review.md` |

---

## 📅 Phase 2 – 자료구조 & OOP [10일 압축] (Day 11 ~ 20)

> 📌 **압축 방침**: 클래스·상속·dataclass는 자동매매 모듈 구조 이해에 필수.  
> 연결리스트·이진탐색 등 순수 알고리즘 주제는 **선택 학습**으로 전환.  
> 참고 파일: `labs/phase2/` (Day 21–40 전체 보관)

| Day | 압축 주제 | 핵심 내용 | 심화 선택 파일 |
|-----|------|----------|----------------|
| 11 | 클래스 기초 + 속성 | class, __init__, self, 인스턴스/클래스 속성 | `day21_class_basic.md`, `day22_class_attr.md` |
| 12 | 상속 + 다형성 | super(), 메서드 오버라이딩, 추상 클래스 (abc) | `day23_inheritance.md`, `day24_polymorphism.md`, `day27_abstract.md` |
| 13 | 캡슐화 + 매직 메서드 | @property, __str__/__repr__/__len__ | `day25_encapsulation.md`, `day26_magic_methods.md` |
| 14 | dataclass + Protocol | @dataclass, field, Protocol, TypedDict | `day45_advanced_types.md` |
| 15 | 스택·큐 + 재귀 | 핵심 자료구조 구현, 재귀 기초 | `day28_stack_queue.md`, `day32_recursion.md` |
| 16 | 컴프리헨션 + 제너레이터 | list/dict/set 컴프리헨션, yield, 이터레이터 | `day33_comprehension.md`, `day34_iterator.md`, `day35_generator.md` |
| 17 | 함수형 + collections | lambda/map/filter/reduce, Counter/deque/defaultdict | `day36_functional.md`, `day38_collections.md` |
| 18 | 정렬 알고리즘 + 해시맵 | 정렬 원리, dict 내부 구조 | `day30_sorting.md`, `day31_hashmap.md` |
| 19 | 미니 프로젝트 | OOP 기반 주식 포트폴리오 관리 클래스 | `day39_project_grade.md` |
| 20 | Phase 2 리뷰 | 코드 리뷰 + 취약점 보완 | `day40_review.md` |

---

## 📅 Phase 3 – Python 고급 & 비동기 [10일 압축] (Day 21 ~ 30)

> 📌 **압축 방침**: 데코레이터·asyncio·Pydantic·dotenv·pytest는 FastAPI·자동매매 필수.  
> GraphQL·고급 제너레이터 등은 **선택 학습**으로 전환.  
> 참고 파일: `labs/phase3/` (Day 41–60 전체 보관)

| Day | 압축 주제 | 핵심 내용 | 심화 선택 파일 |
|-----|------|----------|----------------|
| 21 | 데코레이터 기초 + 심화 | @wrapper, functools.wraps, 인자 있는 데코레이터 | `day41_decorator_basic.md`, `day42_decorator_advanced.md` |
| 22 | 컨텍스트 매니저 + 타입힌트 | with/__enter__/__exit__, Optional/Union/list | `day43_context_manager.md`, `day44_type_hints.md` |
| 23 | Pydantic v2 기초 + 심화 | BaseModel, 유효성 검사, @field_validator | `day46_pydantic_basic.md`, `day47_pydantic_advanced.md` |
| 24 | asyncio 기초 + 심화 | async/await, event loop, gather, Task | `day48_sync_vs_async.md`, `day49_asyncio_basic.md`, `day50_asyncio_advanced.md` |
| 25 | HTTP 클라이언트 | requests GET/POST, httpx 비동기 클라이언트 | `day51_http_basics.md`, `day52_requests.md`, `day53_httpx.md` |
| 26 | 환경변수 + 로깅 | python-dotenv, os.environ, logging 모듈 | `day54_logging.md`, `day55_config.md` |
| 27 | pytest 기초 + 심화 | fixture, parametrize, mock, TestClient | `day56_pytest_basic.md`, `day57_pytest_advanced.md` |
| 28 | 파일 자동화 | PDF (fpdf), Excel (openpyxl), CSV 처리 | `day58_file_automation.md` |
| 29 | 미니 프로젝트 | 비동기 주가 API 클라이언트 + 텔레그램 전송 | `day59_project_weather.md` |
| 30 | Phase 3 리뷰 | 코드 리뷰 + Phase 1–3 종합 점검 | `day60_review.md` |

---

## 📅 Phase 4 – FastAPI 기초 (Day 31 ~ 50)

| Day | 주제 | LAB 파일 |
|-----|------|----------|
| 31 | FastAPI 소개 & 설치 – uvicorn, Swagger UI | `labs/phase4/day61_fastapi_intro.md` |
| 32 | 첫 번째 API – GET /, 자동 문서화 | `labs/phase4/day62_first_api.md` |
| 33 | 경로 매개변수 – Path Parameter, 타입 변환 | `labs/phase4/day63_path_params.md` |
| 34 | 쿼리 매개변수 – Query Parameter, 기본값, Optional | `labs/phase4/day64_query_params.md` |
| 35 | 요청 본문 – Request Body, Pydantic 모델 | `labs/phase4/day65_request_body.md` |
| 36 | 응답 모델 – response_model, status_code | `labs/phase4/day66_response_model.md` |
| 37 | HTTP 메서드 – POST, PUT, PATCH, DELETE | `labs/phase4/day67_http_methods.md` |
| 38 | 폼 데이터 & 파일 업로드 | `labs/phase4/day68_form_file.md` |
| 39 | 헤더 & 쿠키 처리 | `labs/phase4/day69_header_cookie.md` |
| 40 | HTTPException & 에러 핸들러 | `labs/phase4/day70_exception.md` |
| 41 | 미들웨어 – CORS, GZip, 커스텀 미들웨어 | `labs/phase4/day71_middleware.md` |
| 42 | 의존성 주입 – Depends, 중첩 의존성 | `labs/phase4/day72_depends.md` |
| 43 | Router – APIRouter, 태그, prefix | `labs/phase4/day73_router.md` |
| 44 | 백그라운드 태스크 – BackgroundTasks | `labs/phase4/day74_background_tasks.md` |
| 45 | 정적 파일 & Jinja2 템플릿 | `labs/phase4/day75_static_template.md` |
| 46 | JSON 파일 기반 CRUD API (DB 없이) | `labs/phase4/day76_json_crud.md` |
| 47 | API 버전 관리 – prefix /v1, /v2 | `labs/phase4/day77_api_versioning.md` |
| 48 | Uvicorn 심화 – 설정, workers, SSL | `labs/phase4/day78_uvicorn_advanced.md` |
| 49 | 미니 프로젝트 – FastAPI 유저 관리 API | `labs/phase4/day79_project_users.md` |
| 50 | Phase 4 종합 리뷰 & 코드 리뷰 세션 | `labs/phase4/day80_review.md` |

---

## 📅 Phase 5 – FastAPI 중급 (Day 51 ~ 70)

| Day | 주제 | LAB 파일 |
|-----|------|----------|
| 51 | 관계형 DB 기초 – SQLite, SQL 기본 | `labs/phase5/day81_sqlite_basics.md` |
| 52 | SQLAlchemy Core – Engine, Connection, Table | `labs/phase5/day82_sqlalchemy_core.md` |
| 53 | SQLAlchemy ORM – declarative_base, 모델 정의 | `labs/phase5/day83_sqlalchemy_orm.md` |
| 54 | FastAPI + SQLAlchemy – Session, CRUD | `labs/phase5/day84_fastapi_db.md` |
| 55 | Alembic – 마이그레이션, revision, upgrade | `labs/phase5/day85_alembic.md` |
| 56 | 인증 기초 – 패스워드 해싱, passlib, bcrypt | `labs/phase5/day86_auth_password.md` |
| 57 | JWT 발급 & 검증 – python-jose, access/refresh token | `labs/phase5/day87_jwt.md` |
| 58 | OAuth2PasswordBearer – FastAPI 인증 흐름 | `labs/phase5/day88_oauth2.md` |
| 59 | Role 기반 접근 제어(RBAC) | `labs/phase5/day89_rbac.md` |
| 60 | 페이지네이션 & 필터링 – skip/limit, 쿼리 최적화 | `labs/phase5/day90_pagination.md` |
| 61 | 캐싱 – functools.lru_cache, Redis 기초 | `labs/phase5/day91_caching.md` |
| 62 | 비동기 DB – asyncpg, databases 라이브러리 | `labs/phase5/day92_async_db.md` |
| 63 | pytest + TestClient – FastAPI 테스트 | `labs/phase5/day93_testing_api.md` |
| 64 | pytest 고급 – DB fixture, 독립 테스트 DB | `labs/phase5/day94_testing_advanced.md` |
| 65 | API 문서화 심화 – OpenAPI tags, description, examples | `labs/phase5/day95_openapi_docs.md` |
| 66 | 파일 업로드 & S3 연동 기초 | `labs/phase5/day96_file_upload_s3.md` |
| 67 | 이메일 전송 – fastapi-mail, SMTP | `labs/phase5/day97_email.md` |
| 68 | 설정 관리 – pydantic-settings, .env | `labs/phase5/day98_settings.md` |
| 69 | 미니 프로젝트 – JWT 인증 포함 게시판 API | `labs/phase5/day99_project_board.md` |
| 70 | Phase 5 종합 리뷰 & 코드 리뷰 세션 | `labs/phase5/day100_review.md` |

---

## 📅 Phase 6 – FastAPI 고급 & 실전 프로젝트 (Day 71 ~ 90)

| Day | 주제 | LAB 파일 |
|-----|------|----------|
| 71 | WebSocket – 실시간 채팅 기초 | `labs/phase6/day101_websocket.md` |
| 72 | WebSocket 심화 – 룸, 브로드캐스트 | `labs/phase6/day102_websocket_rooms.md` |
| 73 | 비동기 작업 – Celery + Redis 기초 | `labs/phase6/day103_celery.md` |
| 74 | SSE (Server-Sent Events) – 실시간 알림 | `labs/phase6/day104_sse.md` |
| 75 | Docker 기초 – Dockerfile, 이미지, 컨테이너 | `labs/phase6/day106_docker_basic.md` |
| 76 | Docker Compose – FastAPI + DB 멀티 컨테이너 | `labs/phase6/day107_docker_compose.md` |
| 77 | CI/CD – GitHub Actions 파이프라인 | `labs/phase6/day108_cicd.md` |
| 78 | 클라우드 배포 – Railway / Render / Fly.io | `labs/phase6/day109_deploy_cloud.md` |
| 79 | 보안 강화 – Rate Limiting, SQL Injection 방어 | `labs/phase6/day111_security.md` |
| 80 | 모니터링 – Prometheus, Grafana, Sentry | `labs/phase6/day112_monitoring.md` |
| 81 | 최종 프로젝트 설계 – 요구사항 정의, ERD, API 설계 | `labs/phase6/day113_project_design.md` |
| 82 | 최종 프로젝트 개발 1 – 모델 & 인증 구현 | `labs/phase6/day114_project_dev1.md` |
| 83 | 최종 프로젝트 개발 2 – 핵심 API 구현 | `labs/phase6/day115_project_dev2.md` |
| 84 | 최종 프로젝트 개발 3 – 파일 업로드·이메일 | `labs/phase6/day116_project_dev3.md` |
| 85 | 최종 프로젝트 개발 4 – 테스트 작성 | `labs/phase6/day117_project_dev4.md` |
| 86 | 최종 프로젝트 개발 5 – Docker & 배포 | `labs/phase6/day118_project_dev5.md` |
| 87 | 최종 프로젝트 발표 준비 & 코드 리뷰 | `labs/phase6/day119_project_review.md` |
| 88 | 최종 발표 & 수료식 | `labs/phase6/day120_graduation.md` |
| 89 | GraphQL 기초 – Strawberry + FastAPI *(선택)* | `labs/phase6/day105_graphql.md` |
| 90 | 성능 최적화 – 프로파일링, N+1, 인덱스 *(선택)* | `labs/phase6/day110_performance.md` |

---

## 📅 Phase 7 – 금융 데이터 분석 & 머신러닝 (Day 91 ~ 120)

> **구성**: 초급(Day 91–100) → 중급(Day 101–110) → 고급(Day 111–120)

### 🟢 초급 – 금융 데이터 수집 & 정리 (Day 91 ~ 100)

| Day | 주제 | LAB 파일 |
|-----|------|----------|
| 91  | 금융 데이터 개요 – 주식·ETF·암호화폐 기초 개념, 시장 구조 | `labs/phase7/day121_finance_intro.md` |
| 92  | Yahoo Finance API – `yfinance`로 주가·거래량 데이터 수집 | `labs/phase7/day122_yfinance.md` |
| 93  | 한국 증권 API – FinanceDataReader, KIS Open API 기초 | `labs/phase7/day123_korean_api.md` |
| 94  | pandas 기초 – Series, DataFrame, 인덱싱, 슬라이싱 | `labs/phase7/day124_pandas_basic.md` |
| 95  | pandas 시계열 – DatetimeIndex, resample, rolling, shift | `labs/phase7/day125_pandas_timeseries.md` |
| 96  | 데이터 시각화 – matplotlib 주가 차트, plotly 인터랙티브 | `labs/phase7/day126_visualization.md` |
| 97  | 데이터 정제 – 결측값 처리, 이상값 탐지, 정규화 | `labs/phase7/day127_data_cleaning.md` |
| 98  | 기본적 분석 – PER·PBR·EPS·ROE·배당수익률 | `labs/phase7/day128_fundamental.md` |
| 99  | 미니 프로젝트 – 종목 분석 리포트 자동화 (PDF) | `labs/phase7/day129_project_report.md` |
| 100 | 초급 종합 리뷰 | `labs/phase7/day130_review_beginner.md` |

### 🟡 중급 – 기술적 분석 & 백테스트 (Day 101 ~ 110)

| Day | 주제 | LAB 파일 |
|-----|------|----------|
| 101 | 이동평균선(MA) – SMA·EMA, 골든/데드크로스 | `labs/phase7/day131_ma.md` |
| 102 | RSI – 계산 원리, 과매수·과매도 판단 | `labs/phase7/day132_rsi.md` |
| 103 | MACD – MACD선·시그널·히스토그램 | `labs/phase7/day133_macd.md` |
| 104 | 추가 지표 – 볼린저밴드, 스토캐스틱, ATR | `labs/phase7/day134_extra_indicators.md` |
| 105 | 백테스트 기초 – 전략 검증 프레임워크 | `labs/phase7/day135_backtest_basic.md` |
| 106 | 백테스트 심화 – 누적수익률, 샤프지수, MDD | `labs/phase7/day136_backtest_metrics.md` |
| 107 | 자동매매 로직 – 신호 생성, 포지션 관리 기초 | `labs/phase7/day137_auto_trading.md` |
| 108 | 포트폴리오 구성 – 자산 배분, 리밸런싱 | `labs/phase7/day138_portfolio.md` |
| 109 | 미니 프로젝트 – MA+RSI 복합 전략 백테스트 | `labs/phase7/day139_project_backtest.md` |
| 110 | 중급 종합 리뷰 | `labs/phase7/day140_review_intermediate.md` |

### 🔴 고급 – 머신러닝 & 전략 최적화 (Day 111 ~ 120)

| Day | 주제 | LAB 파일 |
|-----|------|----------|
| 111 | ML 기초 – scikit-learn 파이프라인, 특성 엔지니어링 | `labs/phase7/day141_ml_basics.md` |
| 112 | 회귀 모델 – Linear/Random Forest 주가 예측 | `labs/phase7/day142_regression.md` |
| 113 | 분류 모델 – Logistic/XGBoost 상승·하락 예측 | `labs/phase7/day143_classification.md` |
| 114 | 모델 평가 – 교차검증, 과적합, ROC-AUC | `labs/phase7/day144_model_evaluation.md` |
| 115 | 시계열 분석 – 정상성 검정, ARIMA | `labs/phase7/day145_arima.md` |
| 116 | 딥러닝 기초 – 신경망 개념, TensorFlow/Keras | `labs/phase7/day146_dl_basics.md` |
| 117 | LSTM – 시계열 주가 예측 모델 학습 & 평가 | `labs/phase7/day147_lstm.md` |
| 118 | 전략 최적화 – 하이퍼파라미터 튜닝, Optuna | `labs/phase7/day148_optimization.md` |
| 119 | 리스크 관리 이론 – VaR, 포지션 사이징 이론 | `labs/phase7/day149_risk_management.md` |
| 120 | 미니 프로젝트 – AI 투자 분석 시스템 설계 | `labs/phase7/day150_final_project.md` |

### 🧪 Phase 7 보완 확장 모듈 (요청 커리큘럼 반영)

| Day | 주제 | LAB 파일 |
|-----|------|----------|
| 151 | SVM 기반 주가 방향 분류 | `labs/phase7/day151_svm.md` |
| 152 | CNN 기반 시계열 패턴 분류 | `labs/phase7/day152_cnn_timeseries.md` |
| 153 | Transformer 기반 시계열 예측 | `labs/phase7/day153_transformer_timeseries.md` |
| 154 | 종목 클러스터링 (KMeans/DBSCAN) | `labs/phase7/day154_clustering.md` |
| 155 | 주식시장 계절성 분석 (연말랠리·월별·요일효과) | `labs/phase7/day155_seasonality.md` |
| 156 | 네이버 주식 페이지 크롤링 데이터 수집 | `labs/phase7/day156_naver_crawling.md` |

---

## 📅 Phase 8 – 자동매매 시스템 실전 ✨ (Day 121 ~ 150)

> **목표**: EC2 서버에서 24시간 운용 가능한 AI 자동매매 시스템 완성  
> **브로커**: Alpaca (미국 주식) + 키움증권 (국내 주식)  
> **구성**: 1주 = 5일 × 6주

---

### 🟢 1주차 – 환경 구축 & 브로커 API 연동 (Day 121 ~ 125)

| Day | 주제 | LAB 파일 | 핵심 모듈 |
|-----|------|----------|-----------|
| 121 | EC2 인스턴스 생성 + SSH + Python 환경 구성 | `labs/phase8/day121_ec2_setup.md` | – |
| 122 | Alpaca Paper Trading API 키 발급 + 계좌 조회 | `labs/phase8/day122_alpaca_account.md` | `AlpacaTrader.get_account()` |
| 123 | Alpaca 주문 실행 – 시장가·지정가·포지션 청산 | `labs/phase8/day123_alpaca_orders.md` | `AlpacaTrader.market_order()` |
| 124 | 키움증권 OpenAPI+ 기초 + 시뮬레이션 모드 | `labs/phase8/day124_kiwoom_basic.md` | `KiwoomTrader` |
| 125 | AutoTrader 통합 모듈 활용 + 첫 자동매매 | `labs/phase8/day125_autotrader.md` | `AutoTrader` |

---

### 🟡 2주차 – 시장 데이터 & 전략 + 텔레그램 (Day 126 ~ 130)

| Day | 주제 | LAB 파일 | 핵심 모듈 |
|-----|------|----------|-----------|
| 126 | 실시간 시장 데이터 수집 + 지표 계산 파이프라인 | `labs/phase8/day126_market_data.md` | `AlpacaTrader.get_bars()` |
| 127 | MA 크로스 전략 구현 + 백테스트 검증 | `labs/phase8/day127_ma_strategy.md` | `AutoTrader.run_once()` |
| 128 | RSI + MACD 복합 신호 전략 | `labs/phase8/day128_rsi_macd_strategy.md` | `AlpacaTrader.rsi_signal()` |
| 129 | 텔레그램 봇 알림 연동 (체결·신호·에러·일일 결산) | `labs/phase8/day129_telegram.md` | `TelegramNotifier` |
| 130 | APScheduler 자동화 + 일일 결산 알림 스케줄링 | `labs/phase8/day130_scheduler.md` | `BlockingScheduler` |

---

### 🔵 3주차 – AI 모델 통합 (Day 131 ~ 135)

| Day | 주제 | LAB 파일 | 핵심 모듈 |
|-----|------|----------|-----------|
| 131 | 특성 공학 (FeatureBuilder) + 레이블 생성 전략 | `labs/phase8/day131_feature_engineering.md` | `FeatureBuilder` |
| 132 | RandomForest 모델 학습 + 시계열 교차검증 | `labs/phase8/day132_random_forest.md` | `MLStrategy(model_type='rf')` |
| 133 | XGBoost 모델 학습 + RF 성능 비교 | `labs/phase8/day133_xgboost.md` | `MLStrategy(model_type='xgb')` |
| 134 | 모델 저장·불러오기 + EC2 서버 배포 | `labs/phase8/day134_model_deploy.md` | `MLStrategy.save/load()` |
| 135 | AI 신호 기반 자동매매 통합 실행 | `labs/phase8/day135_ai_trading.md` | `MLSignalAdapter` |

---

### 🟠 4주차 – 리스크 관리 + DB 매매 기록 (Day 136 ~ 140)

| Day | 주제 | LAB 파일 | 핵심 모듈 |
|-----|------|----------|-----------|
| 136 | SQLite 매매 기록 – 체결·스냅샷·이벤트 저장 | `labs/phase8/day136_trade_logger.md` | `TradeLogger` |
| 137 | 일일 손실 한도 구현 + 자동 거래 중단 | `labs/phase8/day137_daily_loss_limit.md` | `RiskManager.daily_loss_limit` |
| 138 | MDD 한도 + 시스템 전체 정지 메커니즘 | `labs/phase8/day138_mdd_halt.md` | `RiskManager.max_mdd_limit` |
| 139 | 포지션 사이징 + 쿨다운 + 일일 거래 횟수 제한 | `labs/phase8/day139_position_sizing.md` | `RiskManager.position_size()` |
| 140 | 리스크 관리 + 매매 기록 통합 실전 데모 | `labs/phase8/day140_risk_integration.md` | 전체 통합 |

---

### 🔴 5주차 – 안정성 강화 (Day 141 ~ 145)

| Day | 주제 | LAB 파일 | 핵심 기술 |
|-----|------|----------|-----------|
| 141 | systemd 서비스 등록 + 부팅 시 자동 시작 | `labs/phase8/day141_systemd.md` | `autotrader.service` |
| 142 | 에러 복구 로직 + 재시도 메커니즘 구현 | `labs/phase8/day142_error_recovery.md` | `MAX_RETRIES + backoff` |
| 143 | CloudWatch 로그 모니터링 + 알람 설정 | `labs/phase8/day143_cloudwatch.md` | `amazon-cloudwatch-agent` |
| 144 | 자동 백업 – cron + S3 업로드 설정 | `labs/phase8/day144_backup.md` | `crontab`, `aws s3 sync` |
| 145 | 통합 시스템 테스트 + 의도적 장애 시뮬레이션 | `labs/phase8/day145_system_test.md` | `kill -9`, 복구 검증 |

---

### ⚫ 6주차 – 실전 운용 (Day 146 ~ 150)

| Day | 주제 | LAB 파일 | 핵심 내용 |
|-----|------|----------|-----------|
| 146 | Paper Trading 성과 분석 – 승률·샤프지수·MDD | `labs/phase8/day146_performance.md` | `TradeLogger.print_summary()` |
| 147 | 멀티 전략 포트폴리오 – MA + AI 혼합 운용 | `labs/phase8/day147_multi_strategy.md` | `AutoTrader` 복수 인스턴스 |
| 148 | Live Trading 전환 체크리스트 + 소액 실전 | `labs/phase8/day148_live_trading.md` | `AlpacaTrader(paper=False)` |
| 149 | 실전 모니터링 + 점진적 증액 계획 수립 | `labs/phase8/day149_live_monitoring.md` | 텔레그램 + CloudWatch |
| 150 | 최종 프로젝트 발표 – AI 자동매매 시스템 배포 | `labs/phase8/day150_final_project.md` | 전체 통합 발표 |

### 🧠 Phase 8 보완 확장 모듈 (자산배분/로보어드바이저)

| Day | 주제 | LAB 파일 | 핵심 내용 |
|-----|------|----------|-----------|
| 151 | Risk-Parity 자산배분 모델 구현 | `labs/phase8/day151_risk_parity.md` | 리스크 기여도 균등화 |
| 152 | Black-Litterman 포트폴리오 모델 | `labs/phase8/day152_black_litterman.md` | 시장균형 + 투자자 관점 결합 |
| 153 | 로보어드바이저 포트폴리오 최적화 | `labs/phase8/day153_roboadvisor_optimization.md` | 스크리닝·최적화·리밸런싱 통합 |

## 📅 Phase 9 – PineScript/TradingView 인디케이터 트랙 (추가)

> **목표**: TradingView 기반 전략 설계 → Python 성과 검증 → 자동화 연계

| Day | 주제 | LAB 파일 |
|-----|------|----------|
| 161 | TradingView PineScript 기초 | `labs/phase9/day161_pinescript_basic.md` |
| 162 | 커스텀 인디케이터 설계 및 구현 | `labs/phase9/day162_custom_indicator.md` |
| 163 | PineScript 전략의 Python 성과 검증 | `labs/phase9/day163_pinescript_python_validation.md` |

---

## 🏗️ 일일 LAB 운영 방식

```
08:00 – 10:00  이론 강의    개념 설명 + 라이브 코딩 데모
10:00 – 12:00  LAB 실습 1  단계별 안내 실습 (guided)
12:00 – 13:00  점심 휴식
13:00 – 15:00  LAB 실습 2  자유 실습 + 심화 도전 과제
15:00 – 17:00  과제 작성    오늘 배운 내용으로 과제 완성
17:00 – 18:00  코드 리뷰    강사 피드백 + Q&A
```

---

## 📂 디렉터리 구조

```
.
├── trading/                         # ✨ 자동매매 핵심 모듈 패키지
│   ├── __init__.py
│   ├── alpaca_client.py             # Alpaca Markets API (미국 주식)
│   ├── kiwoom_client.py             # 키움증권 OpenAPI+ (국내 주식)
│   ├── auto_trader.py               # 신호·주문 오케스트레이터
│   ├── telegram_notifier.py         # 텔레그램 알림 (체결·신호·에러·결산)
│   ├── ml_strategy.py               # RandomForest / XGBoost AI 전략
│   ├── risk_manager.py              # 일손실·MDD·포지션 사이징·시스템 정지
│   └── trade_logger.py              # SQLite 매매 기록·스냅샷·CSV 내보내기
├── models/                          # 학습된 ML 모델 (.pkl)
├── data/                            # trading.db (SQLite)
├── logs/                            # 운용 로그
├── labs/
│   ├── phase1/   (Day 01–10 압축)   Python 핵심 기초
│   ├── phase2/   (Day 11–20 압축)   자료구조 & OOP
│   ├── phase3/   (Day 21–30 압축)   Python 고급 & 비동기
│   ├── phase4/   (Day 31–50)        FastAPI 기초
│   ├── phase5/   (Day 51–70)        FastAPI 중급
│   ├── phase6/   (Day 71–90)        FastAPI 고급 & 실전
│   ├── phase7/   (Day 91–120)       금융 데이터 분석 & ML
│   ├── phase8/   (Day 121–150) ✨   자동매매 시스템 실전 (6주)
│   └── phase9/   (추가 트랙)         PineScript 인디케이터 & Python 검증
└── CURRICULUM.md
```

---

## 🛠️ 전체 실습 환경 패키지

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# Phase 1–6: Python + FastAPI 스택
pip install fastapi uvicorn[standard] pydantic sqlalchemy alembic \
            python-jose passlib bcrypt httpx pytest pytest-asyncio \
            python-dotenv pydantic-settings fpdf2

# Phase 7: 금융 데이터 분석 & ML
pip install yfinance FinanceDataReader pandas numpy matplotlib plotly \
            scikit-learn xgboost optuna tensorflow keras \
            backtesting bt statsmodels

# Phase 8: 자동매매 시스템 ✨
pip install alpaca-py \
            pykiwoom \              # Windows 전용 (키움증권)
            python-telegram-bot \
            apscheduler \
            joblib

# 확장 모듈(Phase 7/9): 크롤링·PineScript 검증 보강
pip install beautifulsoup4 lxml requests selenium
```

---

## 📊 평가 기준

| 항목 | 비중 | 설명 |
|------|------|------|
| 일일 LAB 과제 | 40% | 매일 제출하는 실습 결과물 |
| Phase 미니 프로젝트 | 30% | Phase 3·5·7 소규모 프로젝트 |
| 최종 프로젝트 (Day 150) | 30% | AI 자동매매 시스템 EC2 배포 & 발표 |

---

*본 커리큘럼은 `edumgt/Python-FastAPI-Uvicorn` 레포지토리 기반으로 구성되었습니다.*

🔎 유튜브 관련 영상 검색: https://www.youtube.com/results?search_query=python+trading+CURRICULUM
