from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional
from pydantic import Field

class PropertyData(BaseModel):
    """Encapsulates the expected input data for property price prediction."""
    
    zip_code: Optional[str] = None
    province: Literal["antwerp", "brabant_wallon", "brussels", "east_flanders", "hainaut","liege", "limburg", 
                      "luxembourg", "namur", "vlaams_brabant", "west_flanders", "not_specified"
                      ] = "not_specified"
    latitude: float = 0.0
    longitude: float = 0.0

    type_property: Literal["apartment", "house"]
    subtype_property: Literal["apartment", "bungalow", "chalet", "cottage", "duplex", "ground_floor",
                          "loft", "mansion", "master_house", "mixed_building", "penthouse",
                          "residence", "studio", "triplex", "villa"]
    livable_surface: float = Field(gt=0, le=2000, default = 40)
    state_of_property: Literal["excellent", "fully_renovated", "new", "normal", "not_specified",
                           "to_be_renovated", "to_demolish", "to_renovate", "to_restore", "under_construction"
                           ] = "not_specified"
    
    bedrooms: int = Field(ge=0, le=10, default = 1)
    bathrooms: int = Field(ge=0, le=10, default = 1)
    toilets: int = Field(ge=0, le=10, default = 1)
    
    epc_score: Literal["A", "A+", "B", "C", "D", "E", "F", "G", "not_specified"
                       ] = "not_specified"
    heating_type: Literal["coal", "electricity", "fuel_oil", "gas", "hot_air", "not_specified", "solar_energy", "wood"
                      ] = "not_specified"
    sun_exposure: Literal["east", "north", "north_east", "north_west", "not_specified", "south", "south_east", "south_west", "west"
                      ] = "not_specified"
    flooding_area_type: Literal["(information_not_available)", "actual_flooding_area", "low_risk",
                            "no_flooding_area", "possible_flooding_area"
                            ] = "(information_not_available)"
    livable_surface: float = Field(gt=0, le=2000)

    facades: int = Field(ge=0, le=4, default = 2)
    terrace: bool = False
    garden: bool = False
    garage: bool = False
    swimming_pool: bool = False

@model_validator(mode="after")
def check_location(self):
    """Validates the location data provided in the PropertyData model."""
    
    using_zip = self.latitude == 0 and self.longitude == 0

    if using_zip:
        if not self.zip_code:
            raise ValueError("latitude/longitude are 0 — provide a zip_code to resolve them.")
    else:
        if not (49.4 <= self.latitude <= 51.6):
            raise ValueError("latitude must be between 49.4 and 51.6 (or 0 to use zip_code).")
        if not (2.5 <= self.longitude <= 6.2):
            raise ValueError("longitude must be between 2.5 and 6.2 (or 0 to use zip_code).")
    return self