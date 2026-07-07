from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()
model = joblib.load("../model/xgboost.joblib")

class PropertyData(BaseModel):
    province: str
    type_property: str
    subtype_property: str
    state_of_property: str
    heating_type: str
    sun_exposure: str
    epc_score: str
    flooding_area_type: str
    livable_surface: float
    latitude: float
    longitude: float
    facades: int
    bedrooms: int
    bathrooms: int
    toilets: int
    
@app.get("/")
def read_root():
    return "alive"

@app.get("/predict")
def predict(property_data: PropertyData):

    return "predict"