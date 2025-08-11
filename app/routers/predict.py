from fastapi import APIRouter
from ..schemas import PredictRequest, PredictResponse, PredictResponseItem
from ..services.model_service import ModelService

router = APIRouter(prefix="/predict", tags=["predict"])

_model = ModelService("models/trained_model.pkl", "models/feature_names.pkl", "models/VERSION")

@router.post("", response_model=PredictResponse)
def predict(payload: PredictRequest):
    y = _model.predict(payload.rows)
    items = []
    for i, (row, pred) in enumerate(zip(payload.rows, y)):
        items.append(PredictResponseItem(
            index=i, district=row.district, date=row.date, P_pred=float(pred)
        ))
    return PredictResponse(model_version=_model.version, items=items)
