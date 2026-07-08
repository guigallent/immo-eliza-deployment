import pandas as pd
import joblib
from pathlib import Path
from schemas import PropertyData
from geo import resolve_location, resolve_province, resolve_province_from_coordinates
from logger import logger

BASE_DIR = Path(__file__).resolve().parent

ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_DIR = BASE_DIR / "model"

model = joblib.load(MODEL_DIR / "xgboost.joblib")
preprocessor = joblib.load(ARTIFACTS_DIR / "preprocessor.joblib")

def predict(property_data: PropertyData):
    try:
        data = property_data.model_dump()

        if data["latitude"] == 0 and data["longitude"] == 0:
            lat, lon = resolve_location(data["zip_code"])
            data["latitude"] = lat
            data["longitude"] = lon
            derived_province = resolve_province(data["zip_code"])
        else:
            derived_province = resolve_province_from_coordinates(data["latitude"], data["longitude"])

        user_province = data.get("province")
        if user_province and user_province != "not_specified":
            if user_province != derived_province:
                raise ValueError(
                    f"province '{user_province}' does not match the location-derived "
                    f"province '{derived_province}'. Set province to 'not_specified' "
                    f"to let it be inferred automatically."
                )
        else:
            data["province"] = derived_province

        data.pop("zip_code", None)

        df = pd.DataFrame([data])
        processed_data = preprocessor.transform(df)
        prediction = model.predict(processed_data)
        return {"prediction": round(float(prediction[0]), 2)}
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise