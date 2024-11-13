from fastapi import FastAPI, Form, Request
from controller.LungCancerController import router as lung_cancer_prediction_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="./templates/")


app = FastAPI()

app.include_router(lung_cancer_prediction_router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, prediction: str = None):
    return templates.TemplateResponse(
        "index.html", {"request": request, "prediction": prediction}
    )


# run using uvicorn main:app --reload
# or fastapi dev ./main.py
