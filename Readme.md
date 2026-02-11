# Python-001 기술 스택 가이드

이 저장소는 **Python 기초 자료구조 실습 + 간단한 FastAPI 서버 + 파일 자동화 예제**를 함께 담은 학습용 프로젝트입니다.

---

## 1) 핵심 언어 / 런타임

- **Python 3.x (권장: 3.10 이상, 실사용 예시는 3.13 포함)**
  - `venv` 가상환경을 사용해 프로젝트 의존성을 분리합니다.
  - 기본 문법(함수, 리스트/딕셔너리/셋, JSON 처리)을 중심으로 구성되어 있습니다.

---

## 2) 백엔드 웹 프레임워크

- **FastAPI**
  - `app.py`에서 REST API를 구성합니다.
  - 비동기 엔드포인트(`async def`) 기반으로 간단한 데이터 응답을 제공합니다.

- **Uvicorn (ASGI 서버)**
  - FastAPI 앱 실행 서버입니다.
  - 개발 모드에서 `--reload` 옵션을 사용해 코드 변경 시 자동 재시작이 가능합니다.

### 제공 API 엔드포인트

- `GET /` : Hello 메시지 반환
- `GET /user` : `mydata.py`에서 만든 dict 데이터 반환
- `GET /fruits` : `hashtest.py`의 set 처리 결과 반환

---

## 3) 데이터 포맷 / 저장 방식

- **JSON 중심 데이터 처리**
  - `json` 표준 라이브러리로 직렬화/역직렬화 처리
  - `users.json`, `loginusers.json` 파일을 이용한 간단한 로그인 상태 저장

- **파일 기반 저장 (로컬 파일 시스템)**
  - DB 없이 JSON 파일을 직접 읽고 쓰는 구조
  - 학습/프로토타이핑에 적합한 단순 persistence 방식

---

## 4) 표준 라이브러리 사용 기술

- **`json`**: dict ↔ JSON 문자열/파일 변환
- **`os`**: 경로 처리 및 파일 존재 확인

프로젝트는 외부 DB/ORM 없이, 파이썬 내장 모듈로도 충분히 기능을 구현하는 방식에 초점을 둡니다.

---

## 5) 부가 자동화/문서 생성 스택

이 저장소에는 웹 API 외에도 문서 자동화 예제가 포함되어 있습니다.

- **FPDF (`fpdf`)**
  - `pdftest.py`에서 PDF를 생성합니다.
  - 한글 출력용 폰트(`malgun.ttf`)를 직접 지정하는 방식입니다.

- **pywin32 (`win32com`)**
  - `hwptest.py`에서 한글(HWP) COM 자동화를 수행합니다.
  - Windows/HWP 설치 환경에 의존적인 스크립트입니다.

> 즉, 이 저장소는 “웹 백엔드 + 자료구조 학습 + 문서 자동화”가 혼합된 형태입니다.

---

## 6) 의존성 관리

- **requirements.txt** 사용
  - `pip freeze > requirements.txt`로 패키지 버전을 고정하는 형태를 사용합니다.

현재 파일 기준 핵심 패키지 예시:
- `uvicorn`
- `click`, `h11`, `colorama` (uvicorn 실행 관련 하위 의존성)

> 참고: FastAPI/FPDF/pywin32 사용 코드가 존재하므로, 실행 환경에 따라 추가 설치가 필요할 수 있습니다.

---

## 7) 실행/개발 환경

## 가상환경 생성

```bash
c:\Python310\python -m venv venv
c:\Python313\python -m venv venv2
venv\Scripts\activate
```

## 서버 실행

```bash
uvicorn app:app --reload
```

## 설치 패키지 확인

```bash
pip list
pip freeze > requirements.txt
```

---

## 8) 코드 성격 요약

- **학습 친화적 구조**: 자료구조(list/dict/set) 예제가 분리되어 있음
- **실행 진입점 다중 구성**: API 서버, 콘솔 로그인, PDF/HWP 자동화 스크립트가 공존
- **초기 프로젝트 특징**: 단순하고 직관적인 파일 구조, 빠른 실습에 적합

---

## 9) 기술 스택 한 줄 정리

**Python + FastAPI + Uvicorn + JSON 파일 저장 + (FPDF / pywin32 자동화)** 기반의 학습형 프로젝트입니다.
