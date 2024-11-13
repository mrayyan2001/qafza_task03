from pydantic import BaseModel


class LungCancerPrediction(BaseModel):
    prediction: str
