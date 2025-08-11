from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/version")
def version(request: Request):
    svc = getattr(request.app.state, "model_service", None)
    return {
        "model_version": getattr(svc, "version", "unavailable"),
        "features": getattr(svc, "feature_names", [])
    }
