from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings
from app.core.logger import init_logging
from app.services.model_service import ModelService
from app.routers import health, predict

log = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: init logging & load model once
    init_logging()
    log.info("Starting HeatX API")
    try:
        app.state.model_service = ModelService(
            settings.MODEL_PATH, settings.FEATURE_PATH, settings.MODEL_VERSION_FILE
        )
        log.info("Model loaded", extra={"extra": {"model_version": app.state.model_service.version}})
    except Exception as e:
        log.exception("Failed to load model")
        # allow startup but predict will 500
        app.state.model_service = None
    yield
    # Shutdown
    log.info("Shutting down HeatX API")

app = FastAPI(title="HeatX API", version="1.0.0", lifespan=lifespan)

# CORS (open by default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.CORS_ORIGINS in ("*", "") else settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(predict.router)

# ---- Error handlers ----
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    # Typically raised by feature mapping when a required feature is missing
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )
