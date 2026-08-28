import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Agriculture Advisory",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       COLOR VARIABLES
       ======================================================== */

    :root {
        --bg: #f4fbf4;
        --bg2: #e8f5e9;

        --primary: #4caf50;
        --primary-dark: #2e7d32;
        --secondary: #66bb6a;
        --accent: #8bc34a;

        --text: #173d2a;
        --muted: #6f8f7b;

        --input-bg: #eef8ef;

        --border: #cfe4d2;
    }


    /* ========================================================
       GLOBAL
       ======================================================== */

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }


    html {
        scroll-behavior: smooth;
    }


    body {
        font-family: Arial, sans-serif;

        color: var(--text);

        background:
            radial-gradient(
                circle at top left,
                rgba(76, 175, 80, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at top right,
                rgba(139, 195, 74, 0.12),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                var(--bg),
                var(--bg2)
            );

        overflow-x: hidden;

        min-height: 100vh;
    }


    /* ========================================================
       STREAMLIT APP BACKGROUND
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                rgba(76, 175, 80, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at top right,
                rgba(139, 195, 74, 0.12),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #f4fbf4,
                #e8f5e9
            );

        color: var(--text);
    }


    /* ========================================================
       HIDE STREAMLIT TOP HEADER
       ======================================================== */

    header[data-testid="stHeader"] {
        display: none !important;
    }


    .stAppViewContainer {
        padding-top: 0 !important;
    }


    /* ========================================================
       MAIN CONTENT
       ======================================================== */

    .block-container {
        max-width: 1180px;

        padding-top: 1rem !important;
        padding-bottom: 4rem !important;
    }


    /* ========================================================
       HERO BACKGROUND GRID
       ======================================================== */

    .hero-bg-grid {
        position: absolute;

        inset: 0;

        background-image:
            linear-gradient(
                rgba(46, 125, 50, 0.035) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(46, 125, 50, 0.035) 1px,
                transparent 1px
            );

        background-size: 60px 60px;

        opacity: 0.5;

        pointer-events: none;
    }


    /* ========================================================
       EYEBROW
       ======================================================== */

    .eyebrow {
        display: inline-block;

        margin-bottom: 18px;

        color: #2e7d32 !important;

        letter-spacing: 0.14em;

        text-transform: uppercase;

        font-size: 0.85rem;

        font-weight: 700;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1 {
        color: #183f2b !important;
    }


    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #174b2c !important;
    }


    /* ========================================================
       GENERAL TEXT
       ======================================================== */

    .stMarkdown,
    .stMarkdown p,
    .stMarkdown li {
        color: #173d2a !important;
    }


    [data-testid="stCaptionContainer"] {
        color: #6f8f7b !important;
    }


    /* ========================================================
       FIELD PARAMETER LABELS
       ======================================================== */

    .stNumberInput label,
    .stTextInput label {
        color: #174b2c !important;

        font-weight: 500 !important;
    }


    /* ========================================================
       REMOVE NUMBER INPUT + / - BUTTONS
       ======================================================== */

    .stNumberInput button[data-testid="stNumberInputStepDown"],
    .stNumberInput button[data-testid="stNumberInputStepUp"] {
        display: none !important;
    }


    /* ========================================================
       REMOVE HELP / ? ICON
       ======================================================== */

    .stNumberInput button[data-testid="stTooltipIcon"] {
        display: none !important;
    }


    /*
       Additional fallback for Streamlit versions where the
       tooltip button does not expose the exact test ID.
    */

    .stNumberInput [data-testid="stTooltipIcon"] {
        display: none !important;
    }


    /* ========================================================
       NUMBER INPUT OUTER CONTAINER
       ======================================================== */

    .stNumberInput [data-baseweb="input"] {
        background: #eef8ef !important;

        border: 1px solid #e6f2e8 !important;

        border-radius: 12px !important;

        box-shadow: none !important;

        overflow: hidden !important;
    }


    /* ========================================================
       NUMBER INPUT INNER CONTAINER
       ======================================================== */

    .stNumberInput [data-baseweb="input"] > div {
        background: #eef8ef !important;
        border: 1px solid #000000 !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        overflow: hidden !important;
        
    }


    /* ========================================================
       NUMBER VALUES
       ======================================================== */

    .stNumberInput input {
        background: #eef8ef !important;

        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        font-weight: 700 !important;

        font-size: 1rem !important;

        opacity: 1 !important;

        border: none !important;

        outline: none !important;

        box-shadow: none !important;
    }


    /* ========================================================
       TEXT INPUT
       ======================================================== */

    .stTextInput input {
        background: #eef8ef !important;

        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        font-weight: 700 !important;

        border: none !important;

        outline: none !important;

        box-shadow: none !important;
    }


    /* ========================================================
       NUMBER INPUT FOCUS
       ======================================================== */

    .stNumberInput [data-baseweb="input"]:focus-within {
        background: #eef8ef !important;

        border: 1px solid #81c784 !important;

        box-shadow:
            0 0 0 1px rgba(76, 175, 80, 0.20) !important;
    }


    /* ========================================================
       PREDICT BUTTON
       ======================================================== */

    .stButton > button {
        width: 100%;

        min-height: 48px;

        border-radius: 999px;

        border: none;

        background:
            linear-gradient(
                135deg,
                #66bb6a,
                #388e3c
            );

        color: #ffffff !important;

        font-weight: 700;

        transition: 0.3s ease;
    }


    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 10px 25px
            rgba(46, 125, 50, 0.22);
    }


    /* ========================================================
       SUCCESS MESSAGE
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 14px !important;

        background: #228B22 !important;

        border: 1px solid #b9dfc1 !important;

        color: #ffffff !important;
    }


    div[data-testid="stAlert"] p {
        color: #185c2a !important;
    }


    /* ========================================================
       INFO MESSAGE
       ======================================================== */

    div[data-testid="stAlert"] {
        color: #185c2a !important;
    }


    /* ========================================================
       METRIC CARD
       ======================================================== */

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.75) !important;

        border:
            1px solid
            #cfe4d2 !important;

        border-radius: 20px !important;

        padding: 18px !important;

        box-shadow:
            0 8px 25px
            rgba(46, 125, 50, 0.06);
    }


    div[data-testid="stMetric"] label {
        color: #557763 !important;
    }


    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #2e7d32 !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        border-color: #cfe4d2 !important;
    }


    /* ========================================================
       HIDE FOOTER
       ======================================================== */

    footer {
        visibility: hidden;
    }


    /* ========================================================
       HIDE MAIN MENU
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }


    /* ========================================================
       MOBILE
       
       IMPORTANT:
       No different colors are used here.
       The same input styling applies to desktop and mobile.
       ======================================================== */

    @media (max-width: 768px) {

        .stNumberInput input {
            color: #000000 !important;

            -webkit-text-fill-color: #000000 !important;

            font-weight: 700 !important;
        }

        .stNumberInput [data-baseweb="input"] {
            background: #eef8ef !important;

            border: 1px solid #e6f2e8 !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "crop_recommendation_model.pkl"
FEATURE_PATH = BASE_DIR / "models" / "feature_columns.pkl"


@st.cache_resource
def load_model():

    model = joblib.load(MODEL_PATH)

    feature_columns = joblib.load(FEATURE_PATH)

    return model, feature_columns


try:

    model, feature_columns = load_model()

except FileNotFoundError:

    st.error(
        "Model files were not found."
    )

    st.info(
        "Please make sure your project contains:\n\n"
        "models/crop_recommendation_model.pkl\n\n"
        "models/feature_columns.pkl"
    )

    st.stop()


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    '<div class="hero-bg-grid"></div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="eyebrow">SMART AGRICULTURE • ML RECOMMENDATION</div>',
    unsafe_allow_html=True
)


st.markdown(
    "# Find the right <span style='color:#2e7d32;'>crop</span> for your soil.",
    unsafe_allow_html=True
)


st.markdown(
    """
    Enter the soil nutrient and environmental conditions of your
    field to receive a machine-learning based crop recommendation.
    """
)


# ============================================================
# SPACING
# ============================================================

st.write("")


# ============================================================
# SECTION TITLE
# ============================================================

st.markdown("## 🌱 Crop Recommendation")

st.write("")


# ============================================================
# TWO COLUMN LAYOUT
# ============================================================

input_column, result_column = st.columns(
    [1.1, 0.9],
    gap="large"
)


# ============================================================
# INPUT SECTION
# ============================================================

with input_column:

    st.subheader("Field Parameters")

    st.caption(
        "Enter the values measured or estimated for your field."
    )


    # ========================================================
    # ROW 1
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        N = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            max_value=200.0,
            value=90.0,
            step=1.0,
            help="Nitrogen content in the soil."
        )


    with col2:

        P = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            max_value=150.0,
            value=42.0,
            step=1.0,
            help="Phosphorus content in the soil."
        )


    # ========================================================
    # ROW 2
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        K = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            max_value=210.0,
            value=43.0,
            step=1.0,
            help="Potassium content in the soil."
        )


    with col2:

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=-10.0,
            max_value=60.0,
            value=25.0,
            step=0.1,
            help="Temperature in degrees Celsius."
        )


    # ========================================================
    # ROW 3
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=80.0,
            step=0.1,
            help="Relative humidity percentage."
        )


    with col2:

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1,
            help="Soil pH value."
        )


    # ========================================================
    # ROW 4
    # ========================================================

    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        max_value=500.0,
        value=200.0,
        step=1.0,
        help="Rainfall in millimeters."
    )


    st.write("")


    # ========================================================
    # PREDICT BUTTON
    # ========================================================

    predict_button = st.button(
        "Predict Crop 🌱",
        use_container_width=True
    )


# ============================================================
# RESULT SECTION
# ============================================================

with result_column:

    st.subheader("Prediction Result")

    st.caption(
        "Your recommended crop and prediction confidence "
        "will appear here."
    )


    if predict_button:

        # ====================================================
        # INPUT DATAFRAME
        # ====================================================

        input_data = pd.DataFrame(
            [{
                "N": N,
                "P": P,
                "K": K,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            }]
        )


        # ====================================================
        # ENSURE FEATURE ORDER
        # ====================================================

        input_data = input_data[feature_columns]


        # ====================================================
        # PREDICT
        # ====================================================

        prediction = model.predict(input_data)[0]


        # ====================================================
        # PROBABILITIES
        # ====================================================

        probabilities = model.predict_proba(input_data)[0]

        classes = model.classes_


        ranked_predictions = sorted(
            zip(classes, probabilities),
            key=lambda x: x[1],
            reverse=True
        )


        confidence = ranked_predictions[0][1] * 100


        # ====================================================
        # RECOMMENDED CROP
        # ====================================================

        st.success(
            f"Recommended Crop: {str(prediction).title()}"
        )


        # ====================================================
        # CONFIDENCE
        # ====================================================

        st.metric(
            "Prediction Confidence",
            f"{confidence:.2f}%"
        )


        # ====================================================
        # TOP 3 RECOMMENDATIONS
        # ====================================================

        st.markdown("### Top 3 Recommendations")


        for rank, (crop, probability) in enumerate(
            ranked_predictions[:3],
            start=1
        ):

            col_a, col_b = st.columns([3, 1])


            with col_a:

                st.write(
                    f"**{rank}. {str(crop).title()}**"
                )


            with col_b:

                st.write(
                    f"**{probability * 100:.2f}%**"
                )


    else:

        st.info(
            "Enter your field conditions and click "
            "'Predict Crop 🌱' to see the recommendation."
        )


# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()


st.markdown("## How it works")


st.markdown(
    """
    The system analyzes soil and environmental conditions using
    a trained machine-learning classification model.
    """
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("### 🧪 Soil Parameters")

    st.write(
        "Nitrogen, phosphorus, potassium and soil pH "
        "are used to understand the soil conditions."
    )


with col2:

    st.markdown("### 🌦️ Environmental Conditions")

    st.write(
        "Temperature, humidity and rainfall provide "
        "information about the growing environment."
    )


with col3:

    st.markdown("### 🤖 ML Prediction")

    st.write(
        "A trained Random Forest classifier analyzes "
        "the parameters and recommends suitable crops."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "Smart Agriculture Advisory • Powered by Machine Learning 🌱"
)
