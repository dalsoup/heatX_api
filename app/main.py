from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logger import init_logging
from app.services.model_service import ModelService
from app.routers import health, predict

log = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_logging()
    log.info("Starting HeatX API")
    try:
        app.state.model_service = ModelService(
            settings.MODEL_PATH, settings.FEATURE_PATH, settings.MODEL_VERSION_FILE
        )
        log.info(
            "Model loaded",
            extra={"extra": {"model_version": app.state.model_service.version}},
        )
    except Exception:
        log.exception("Failed to load model")
        app.state.model_service = None
    yield
    # Shutdown
    log.info("Shutting down HeatX API")

# ✅ 먼저 app을 만든다
app = FastAPI(title="HeatX API", version="1.0.0", lifespan=lifespan)

# ✅ CORS는 한 번만 추가 (원하면 특정 도메인만 허용)
#   - settings.CORS_ORIGINS가 "*" 또는 빈 문자열이면 전체 허용
allow_origins = (
    ["*"]
    if settings.CORS_ORIGINS in ("*", "")
    else [o.strip() for o in settings.CORS_ORIGINS.split(",")]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(health.router)
app.include_router(predict.router)

# 에러 핸들러
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})
