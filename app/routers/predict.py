from fastapi import APIRouter, Request
from ..schemas import PredictRequest, PredictResponse, PredictResponseItem

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post("", response_model=PredictResponse)
def predict(payload: PredictRequest, request: Request):
    svc = getattr(request.app.state, "model_service", None)
    if svc is None:
        # Model failed to load at startup
        return {"model_version": "unavailable", "items": []}
    y = svc.predict(payload.rows)
    items = []
    for i, (row, pred) in enumerate(zip(payload.rows, y)):
        items.append(PredictResponseItem(
            index=i, district=row.district, date=row.date, P_pred=float(pred)
        ))
    return {"model_version": svc.version, "items": items}
