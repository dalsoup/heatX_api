from pydantic import BaseModel, Field
from typing import List, Optional

class Row(BaseModel):
    district: Optional[str] = None
    date: Optional[str] = None
    TMX: float = Field(..., description="최고기온(°C)")
    TMN: float = Field(..., description="최저기온(°C)")
    REH: float = Field(..., ge=0, le=100, description="습도(%)")
    S: float = Field(..., ge=0, le=1, description="사회적 취약지수")
    E: float = Field(..., ge=0, le=1, description="환경적 취약지수")

class PredictRequest(BaseModel):
    rows: List[Row]

class PredictResponseItem(BaseModel):
    index: int
    district: Optional[str] = None
    date: Optional[str] = None
    P_pred: float

class PredictResponse(BaseModel):
    model_version: str
    items: List[PredictResponseItem]
