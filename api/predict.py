import pandas as pd
import joblib
from schemas import PropertyData
import logger

model = joblib.load("../model/xgboost.joblib")
preprocessor = joblib.load("../artifacts/preprocessor.joblib")

def predict(property_data: PropertyData):
    try:
        df = pd.DataFrame([property_data.model_dump()])
        processed_data = preprocessor.transform(df)
        prediction = model.predict(processed_data)
        return {"prediction": float(prediction[0])}
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise