from fastapi import APIRouter, HTTPException, UploadFile, File
from PIL import Image
import numpy as np
from typing import Annotated
import cv2
from tensorflow.keras.models import load_model  # type: ignore
from model.LungCancerModel import LungCancerModel
from view.LungCancerPrediction import LungCancerPrediction

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

# load the model once
router = APIRouter()

model = LungCancerModel()

template = Jinja2Templates(directory="./templates/")


@router.post(
    "/predict",
    # response_model=LungCancerPrediction,
    response_class=HTMLResponse,
)
async def root(request: Request, img_file: UploadFile = File(...)):
    try:
        await model.load_image(img_file.file)
        await model.preprocessing()
        prediction = await model.get_prediction()
        print(prediction)
        # return LungCancerPrediction(prediction=prediction)
        return template.TemplateResponse(
            "index.html", {"request": request, "prediction": prediction}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
