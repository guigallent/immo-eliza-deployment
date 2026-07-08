import pandas as pd
from pathlib import Path

csv_path = Path(__file__).resolve().parent / "artifacts" / "zipcode_belgium.csv"
df = pd.read_csv(csv_path, header=None, names=["zip_code", "city", "longitude", "latitude"], dtype={"zip_code": str},)
zip_code_by_province = [
    (1000, 1299, "brussels"),
    (1300, 1499, "brabant_wallon"),
    (1500, 1999, "vlaams_brabant"),
    (2000, 2999, "antwerp"),
    (3000, 3499, "vlaams_brabant"),
    (3500, 3999, "limburg"),
    (4000, 4999, "liege"),
    (5000, 5999, "namur"),
    (6000, 6599, "hainaut"),
    (6600, 6999, "luxembourg"),
    (7000, 7999, "hainaut"),
    (8000, 8999, "west_flanders"),
    (9000, 9999, "east_flanders"),
]

def resolve_location(zip_code: str) -> tuple[float, float]:
    """Returns (latitude, longitude) for a given zip code."""

    match = df[df["zip_code"] == str(zip_code).strip()]
    if match.empty:
        raise ValueError(f"Could not resolve location for zip_code={zip_code!r}")

    latitude = float(match["latitude"].mean())
    longitude = float(match["longitude"].mean())
    return latitude, longitude

def resolve_province(zip_code: str) -> str:
    """Resolves the Belgian province name associated with a given zip code."""

    code = int(zip_code)
    for low, high, province in zip_code_by_province:
        if low <= code <= high:
            return province
    raise ValueError(f"Could not resolve province for zip_code={zip_code!r}")

def resolve_province_from_coordinates(latitude: float, longitude: float) -> str:
    """Finds the closest known zip code to given coordinates and derives its province."""

    distances = (df["latitude"] - latitude) ** 2 + (df["longitude"] - longitude) ** 2
    nearest_zip = df.loc[distances.idxmin(), "zip_code"]
    return resolve_province(nearest_zip)