import streamlit as st
import requests

# Local Backend URL
BACKEND_URL = "https://churn-backend-api.onrender.com"

# 1. CSS for Hand Pointers (applied to inputs and help icons)
st.markdown("""
    <style>
    /* Targets dropdowns, radio buttons, sliders, and the help (?) icons */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="select"] *,
    [data-baseweb="popover"] li,
    div[role="option"],
    .stSlider > div,
    button,
    .stRadio label,
    .stTooltipIcon {
        cursor: pointer !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Subscription Retention AI")
st.write("Hover over the **(?)** icons to see feature descriptions.")

# 2. Input UI with Help Icons
col1, col2 = st.columns(2)

with col1:
    usage = st.slider(
        "Monthly Usage (Hours)", 0, 100, 25, 
        help="Total hours the customer spent using the service in the last 30 days."
    )
    sub_type = st.selectbox(
        "Plan Tier", ["Basic", "Standard", "Premium"], 
        help="The current billing level of the customer. Premium users typically churn less."
    )
    gender = st.selectbox(
        "Gender", ["M", "F"], 
        help="Customer's self-identified gender."
    )

with col2:
    age = st.number_input(
        "Age", 18, 100, 30, 
        help="Customer's age. Loyalty patterns often vary by age demographic."
    )
    support = st.number_input(
        "Support Calls", 0, 15, 1, 
        help="Number of times the customer contacted support. High volume often indicates frustration."
    )

model_choice = st.radio(
    "Intelligence Model", ["logistic", "decision_tree"], 
    horizontal=True,
    help="Select 'logistic' for statistical probability or 'decision_tree' for logic-based rules."
)

# 3. Prediction Logic
if st.button("Run Analysis"):
    payload = {
        "Usage_Hours": usage,
        "Subscription_Type": sub_type,
        "Age": age,
        "Support_Calls": support,
        "Gender": gender
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/{model_choice}", json=payload)
        
        if response.status_code == 200:
            prediction = response.json()["prediction"]
            if prediction == 1:
                st.error("🚨 **Result:** Customer is likely to **CHURN**.")
            else:
                st.success("✅ **Result:** Customer is likely to **STAY**.")
        else:
            st.warning(f"Backend Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Connection Failed! Ensure the FastAPI backend is running at https://churn-backend-api.onrender.com")
