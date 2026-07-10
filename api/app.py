from fastapi import FastAPI, HTTPException
from schemas import PropertyData
from predict import predict
from logger import logger


app = FastAPI()

@app.get("/")
def read_root():
    """Health check endpoint to verify that the API is running."""

    logger.info("Health check hit.")
    return "alive"

@app.post("/predict")
def predict_price(property_data: PropertyData):
    """Endpoint to predict the price of a property based on the provided data."""

    logger.info(f"Prediction requested: {property_data.model_dump()}")
    try:
        result = predict(property_data)
        logger.info(f"Prediction successful: {result}")
        return result
    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction failed. Please check your input data.")