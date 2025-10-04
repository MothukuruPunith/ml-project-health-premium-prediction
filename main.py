import streamlit as st
from prediction_helper import predict

# --- Page Configuration ---
st.set_page_config(
    page_title="Health Premium Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS (Compact, Professional Dark Mode) ---
st.markdown("""
<style>
    /* Base Styling */
    body {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif;
        margin: 0;
        padding: 0;
    }

    /* Remove Streamlit padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Main container */
    .main-container {
        background-color: #161b22;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        border: 1px solid #30363d;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
    }

    /* Title */
    .title {
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        color: #f0f6fc;
        margin-bottom: 0.2rem;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    /* Section headers */
    h2 {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f0f6fc;
        margin-bottom: 0.6rem;
        border-left: 4px solid #6f42c1;
        padding-left: 10px;
    }

    /* Input fields */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input {
        background-color: #0d1117;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 0.3rem 0.5rem;
        font-size: 0.9rem;
    }

    .stSelectbox>div>div {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 6px;
        font-size: 0.9rem;
    }

    /* Button */
    .stButton>button {
        width: 100%;
        height: 2.5rem;
        border-radius: 8px;
        border: none;
        font-size: 1rem;
        font-weight: 600;
        color: #fff;
        background: linear-gradient(135deg, #6f42c1, #9d6fe4);
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 8px rgba(111, 66, 193, 0.4);
        margin-top: 0.5rem;
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(111, 66, 193, 0.5);
    }

    /* Result box */
    .result-container {
        margin-top: 1rem;
        padding: 1.2rem;
        background-color: #161b22;
        border-left: 5px solid #6f42c1;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #30363d;
    }

    .result-text {
        font-size: 1rem;
        color: #c9d1d9;
        margin-bottom: 0.4rem;
    }

    .result-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #8b949e;
        font-size: 0.85rem;
        margin-top: 1rem;
    }

</style>
""", unsafe_allow_html=True)

# --- App Layout ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<p class="title">Health Premium Prediction</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Fill in the details below to predict your health insurance premium.</p>', unsafe_allow_html=True)
st.markdown("---")

# --- Dropdown Options ---
options_dict = {
    'Gender': ['Male', 'Female'],
    'Region': ['Northeast', 'Northwest', 'Southeast', 'Southwest'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Overweight', 'Underweight', 'Obesity'],
    'Smoking Status': ['No Smoking', 'Occasional', 'Regular'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Medical History': [
        'No Disease',
        'High blood pressure',
        'Diabetes',
        'Heart disease',
        'Thyroid',
        'Diabetes & High blood pressure',
        'Diabetes & Heart disease',
        'Diabetes & Thyroid',
        'High blood pressure & Heart disease'
    ],
    'Insurance Plan': ['Silver', 'Bronze', 'Gold'],
}

# --- Compact 3-column layout ---
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.header("👤 Personal Info")
    age = st.number_input("Age", min_value=1, max_value=100, value=30, step=1)
    gender = st.selectbox("Gender", options=options_dict['Gender'])
    marital_status = st.selectbox("Marital Status", options=options_dict['Marital Status'])
    number_of_dependants = st.number_input("Dependants", min_value=0, max_value=20, value=0, step=1)

with col2:
    st.header("❤️‍🩹 Lifestyle & Financials")
    bmi_category = st.selectbox("BMI Category", options=options_dict['BMI Category'])
    smoking_status = st.selectbox("Smoking Status", options=options_dict['Smoking Status'])
    employment_status = st.selectbox("Employment Status", options=options_dict['Employment Status'])
    income_lakhs = st.number_input("Income (Lakhs/Year)", min_value=1.0, value=10.0, step=0.5, format="%.1f")

with col3:
    st.header("🏥 Medical & Insurance")
    medical_history = st.selectbox("Medical History", options=options_dict['Medical History'])
    genetical_risk = st.number_input("Genetical Risk", min_value=0, max_value=10, value=3, step=1)
    region = st.selectbox("Region", options=options_dict['Region'])
    insurance_plan = st.selectbox("Insurance Plan", options=options_dict['Insurance Plan'])

# --- Data Dictionary ---
user_data = {
    'age': age,
    'number_of_dependants': number_of_dependants,
    'income_lakhs': income_lakhs,
    'genetical_risk': genetical_risk,
    'insurance_plan': insurance_plan,
    'employment_status': employment_status,
    'gender': gender,
    'marital_status': marital_status,
    'bmi_category': bmi_category,
    'smoking_status': smoking_status,
    'region': region,
    'medical_history': medical_history
}

# --- Predict Button ---
if st.button("Predict Premium"):
    with st.spinner('Calculating your premium...'):
        try:
            prediction = predict(user_data)
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.markdown('<p class="result-text">Predicted Annual Premium</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="result-value">₹ {prediction:,.0f}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("<p class='footer'>Built with Streamlit | Health Premium Prediction Tool</p>", unsafe_allow_html=True)
