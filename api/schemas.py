from pydantic import BaseModel
from typing import Literal
from pydantic import Field

class PropertyData(BaseModel):
    """Encapsulates the expected input data for property price prediction."""
    
    province: Literal["antwerp", "brabant_wallon", "brussels", "east_flanders", "hainaut",
                 "liege", "limburg", "luxembourg", "namur", "vlaams_brabant", "west_flanders"]
    type_property: Literal["apartment", "house"]
    subtype_property: Literal["apartment", "bungalow", "chalet", "cottage", "duplex", "ground_floor",
                          "loft", "mansion", "master_house", "mixed_building", "penthouse",
                          "residence", "studio", "triplex", "villa"]
    state_of_property: Literal["excellent", "fully_renovated", "new", "normal", "not_specified",
                           "to_be_renovated", "to_demolish", "to_renovate", "to_restore",
                           "under_construction"]
    heating_type: Literal["coal", "electricity", "fuel_oil", "gas", "hot_air", "not_specified",
                      "solar_energy", "wood"]
    sun_exposure: Literal["east", "north", "north_east", "north_west", "not_specified", "south",
                      "south_east", "south_west", "west"]
    epc_score: Literal["A", "A+", "B", "C", "D", "E", "F", "G", "not_specified"]
    flooding_area_type: Literal["(information_not_available)", "actual_flooding_area", "low_risk",
                            "no_flooding_area", "possible_flooding_area"]
    livable_surface: float = Field(gt=0, le=2000)
    latitude: float = Field(ge=49.4, le=51.6)
    longitude: float = Field(ge=2.5, le=6.2)
    facades: int = Field(ge=0, le=4)
    bedrooms: int = Field(ge=0, le=10)
    bathrooms: int = Field(ge=0, le=10)
    toilets: int = Field(ge=0, le=10)
    terrace: bool
    garden: bool
    garage: bool
    swimming_pool: bool