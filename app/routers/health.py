from fastapi import APIRouter
from ..services.model_service import ModelService

router = APIRouter(tags=["health"])
_model = ModelService("models/trained_model.pkl", "models/feature_names.pkl", "models/VERSION")

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/version")
def version():
    return {"model_version": _model.version, "features": _model.feature_names}
