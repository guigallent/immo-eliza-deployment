import streamlit as st
import requests

st.set_page_config(
    page_title="Immo Eliza — Price Estimator",
    page_icon="🏠",
    layout="centered",
)

API_URL = "https://immo-eliza-deployment-jsgk.onrender.com"

# --------------------------------------------------------------------------
# Page styling in CSS
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .block-container {padding-top: 2.5rem; max-width: 720px;}
        h1 {font-weight: 700;}
        div[data-testid="stMetricValue"] {font-size: 2.6rem; color: #1f6f43;}
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            padding: 0.6rem 0;
            font-weight: 600;
        }
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Option lists (aligned with api/schemas.py)
# --------------------------------------------------------------------------
SUBTYPES = [
    "apartment", "bungalow", "chalet", "cottage", "duplex", "ground_floor",
    "loft", "mansion", "master_house", "mixed_building", "penthouse",
    "residence", "studio", "triplex", "villa"
]
STATES = [
    "not_specified", "new", "excellent", "fully_renovated", "normal",
    "to_be_renovated", "to_renovate", "to_restore", "to_demolish",
    "under_construction"
]
EPC_SCORES = ["not_specified", "A+", "A", "B", "C", "D", "E", "F", "G"]
HEATING_TYPES = [
    "not_specified", "gas", "electricity", "fuel_oil", "hot_air",
    "solar_energy", "wood", "coal"
]
SUN_EXPOSURES = [
    "not_specified", "north", "north_east", "east", "south_east",
    "south", "south_west", "west", "north_west"
]
FLOODING_TYPES = [
    "(information_not_available)", "no_flooding_area", "low_risk",
    "possible_flooding_area", "actual_flooding_area"
]
PROVINCES = [
    "not_specified", "antwerp", "brabant_wallon", "brussels",
    "east_flanders", "hainaut", "liege", "limburg", "luxembourg",
    "namur", "vlaams_brabant", "west_flanders"
]

def label(value: str) -> str:
    """Cleans labels for display in the UI to make them more human-readable."""
    return value.replace("_", " ").replace("(information not available)", "Not available").capitalize()

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.title("🏠 Immo Eliza Price Predictor")
st.caption("Get an instant price estimate for a property in Belgium.")

# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
st.sidebar.header("ℹ️ About Immo Eliza")
st.sidebar.write("Immo Eliza is a tool that provides instant price estimates for properties in Belgium. It connects through an API to a machine learning model trained on real estate data to predict Belgian property prices based on their features.")

st.sidebar.header("⚙️ How to use")
st.sidebar.write("1. Fill in the property details.")
st.sidebar.write("2. Provide the location information.")
st.sidebar.write("3. Check the extra details.")
st.sidebar.write("4. Click \"Submit\" to get an instant price estimate. The first time you submit, it may take some seconds to connect to the model.")

# --------------------------------------------------------------------------
# Form
# --------------------------------------------------------------------------
with st.form("property_form"):

    st.subheader("Property")
    col1, col2 = st.columns(2)
    with col1:
        type_property = st.selectbox("Type", ["apartment", "house"], format_func=label)
    with col2:
        subtype_property = st.selectbox("Subtype", SUBTYPES, format_func=label)

    col1, col2 = st.columns(2)
    with col1:
        livable_surface = st.number_input(
            "Livable surface (m²)", min_value=1.0, max_value=2000.0, value=40.0, step=5.0
        )
    with col2:
        state_of_property = st.selectbox("State of property", STATES, format_func=label)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=1)
    with col2:
        bathrooms = st.number_input("Bathrooms", min_value=0, max_value=10, value=1)
    with col3:
        toilets = st.number_input("Toilets", min_value=0, max_value=10, value=1)
    with col4:
        facades = st.number_input("Facades", min_value=0, max_value=4, value=2)

    st.markdown("**Amenities**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        terrace = st.checkbox("Terrace")
    with col2:
        garden = st.checkbox("Garden")
    with col3:
        garage = st.checkbox("Garage")
    with col4:
        swimming_pool = st.checkbox("Pool")

    st.divider()
    st.subheader("Location")

    location_mode = st.radio(
        "How do you want to provide the location?",
        ["Zip code", "Coordinates"],
        horizontal=True,
    )

    zip_code = None
    latitude, longitude = 0.0, 0.0

    if location_mode == "Zip code":
        zip_code = st.text_input("Zip code", placeholder="e.g. 1000")
    else:
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Latitude", min_value=49.4, max_value=51.6, value=50.85, format="%.5f")
        with col2:
            longitude = st.number_input("Longitude", min_value=2.5, max_value=6.2, value=4.35, format="%.5f")

    province = st.selectbox(
        "Province (leave as 'Not specified' to infer it automatically)",
        PROVINCES,
        format_func=label,
    )

    st.divider()
    st.subheader("Extra details")
    col1, col2 = st.columns(2)
    with col1:
        epc_score = st.selectbox("EPC score (optional)", EPC_SCORES, format_func=label)
        heating_type = st.selectbox("Heating type (optional)", HEATING_TYPES, format_func=label)
    with col2:
        sun_exposure = st.selectbox("Sun exposure (optional)", SUN_EXPOSURES, format_func=label)
        flooding_area_type = st.selectbox("Flood risk area (optional)", FLOODING_TYPES, format_func=label)

    submitted = st.form_submit_button("Estimate price")

# --------------------------------------------------------------------------
# Submit & call API
# --------------------------------------------------------------------------
if submitted:
    if location_mode == "Zip code" and not zip_code:
        st.error("Please provide a zip code, or switch to entering coordinates directly.")
        st.stop()

    payload = {
        "zip_code": zip_code,
        "province": province,
        "latitude": latitude,
        "longitude": longitude,
        "type_property": type_property,
        "subtype_property": subtype_property,
        "livable_surface": livable_surface,
        "state_of_property": state_of_property,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "toilets": toilets,
        "epc_score": epc_score,
        "heating_type": heating_type,
        "sun_exposure": sun_exposure,
        "flooding_area_type": flooding_area_type,
        "facades": facades,
        "terrace": terrace,
        "garden": garden,
        "garage": garage,
        "swimming_pool": swimming_pool,
    }

    with st.spinner("Connecting to the model..."):
        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            st.success("Estimate ready")
            st.metric("Estimated price", f"€ {result['prediction']:,.0f}")
        except requests.exceptions.HTTPError:
            try:
                detail = response.json().get("detail", response.text)
            except ValueError:
                detail = response.text
            st.error(f"The API rejected the request: {detail}")
        except requests.exceptions.ConnectionError:
            st.error(
                "Could not reach the API. Check that API_URL is set correctly "
                f"(currently `{API_URL}`) and that the service is running."
            )
        except requests.exceptions.Timeout:
            st.error("The API took too long to respond. Please try again.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

st.divider()
st.caption(f"Connected API: {API_URL}")