from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io
import tempfile
import os

from utils import predict_leaf

app = FastAPI(title="AgriVision API")


@app.get("/")
def home():
    return {"message": "AgriVision API is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...), language: str = "English"):
    try:
        # Save uploaded image temporarily
        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(await file.read())
            temp_path = temp.name

        result = predict_leaf(temp_path, language=language)

        os.remove(temp_path)

        return JSONResponse(
    {
        "prediction": result["prediction"],
        "disease_name": result["disease_name"],
        "confidence": result["confidence"],
        "severity": result["severity"],
        "severity_level": result["severity_level"],
        "medicine": result["medicine"],
        "dosage": result["dosage"],
        "steps": result["steps"],
        "overlay_path": result["overlay_path"],
    }
)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )