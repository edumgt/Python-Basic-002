"""ML/DL 마이크로서비스 진입점.

실행:
    uvicorn services.ml_service:app --host 0.0.0.0 --port 8000

K8s Deployment args:
    ["uvicorn", "services.ml_service:app", "--host", "0.0.0.0", "--port", "8000"]
"""

from __future__ import annotations

import logging
from importlib import import_module
from os import getenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

app = FastAPI(
    title="ML/DL Service",
    description="머신러닝 및 딥러닝 주가 예측 마이크로서비스",
    version="1.0.0",
)

# CORS_ORIGINS 환경 변수로 허용 오리진을 제어합니다.
# 기본값 "*"는 개발 환경용이며, 프로덕션에서는 실제 도메인으로 제한하세요.
# 예: CORS_ORIGINS="https://myapp.example.com,https://api.example.com"
_cors_origins = [o.strip() for o in getenv("CORS_ORIGINS", "*").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

_ROUTERS = [
    "api.routers.ml_strategy",
    "api.routers.dl_strategy",
]

# 선택적 라우터 로딩: 특정 의존성이 없어도 서비스가 부분 기능으로 시작할 수 있도록
# api.main:app 과 동일한 graceful degradation 패턴을 따릅니다.
for _path in _ROUTERS:
    try:
        _mod = import_module(_path)
        app.include_router(_mod.router)
    except Exception as exc:
        logger.warning("라우터 로드 건너뜀 (%s): %s", _path, exc)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "ml-service"}
