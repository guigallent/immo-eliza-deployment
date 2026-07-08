from fastapi import FastAPI, HTTPException
import logger
from schemas import PropertyData
from predict import predict
from logger import logger


app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Health check hit.")
    return "alive"

@app.post("/predict")
def predict_price(property_data: PropertyData):
    # sourcery skip: raise-from-previous-error
    logger.info(f"Prediction requested: {property_data.model_dump()}")
    try:
        result = predict(property_data)
        logger.info(f"Prediction successful: {result}")
        return result
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction failed. Please check your input data.")