import streamlit as st
import requests
from pages.dashboard import show_dashboard  # Import dashboard function

# ✅ Set page config (hide Streamlit’s built-in navigation)
st.set_page_config(page_title="Student Performance", layout="wide")

# ✅ Remove default Streamlit sidebar navigation
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stDecoration"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ✅ Backend API URL (Update to match your Django backend)
API_BASE_URL = "https://finalproject-production-171c.up.railway.app/api/users/"

# ✅ Initialize session state
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
    st.session_state["username"] = None
    st.session_state["page"] = "login"

is_authenticated = st.session_state["auth_token"] is not None

# ✅ Custom Sidebar Navigation
with st.sidebar:
    st.title("Navigation")

    if is_authenticated:
        if st.button("📊 Dashboard"):
            st.session_state["page"] = "dashboard"
            st.rerun()
        if st.button("🚪 Logout"):
            st.session_state["auth_token"] = None
            st.session_state["username"] = None
            st.session_state["page"] = "login"
            st.toast("Logged out successfully!")
            st.rerun()
    else:
        if st.button("🔑 Login"):
            st.session_state["page"] = "login"
            st.rerun()
        if st.button("📝 Register"):
            st.session_state["page"] = "register"
            st.rerun()

# ✅ Page Routing Logic
API_PREDICT_URL = "https://finalproject-production-171c.up.railway.app/api/predictor/predict/"

# In the page routing logic
if st.session_state["page"] == "dashboard" and is_authenticated:
    show_dashboard(API_PREDICT_URL)  # Pass the URL as an argument

elif st.session_state["page"] == "register":
    st.title("📝 Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["student", "professor"])

    if st.button("Register"):
        try:
            response = requests.post(f"{API_BASE_URL}register/", json={
                "username": username,
                "email": email,
                "password": password,
                "role": role
            })
            if response.status_code == 201:
                st.success("✅ Registration successful! Please login.")
                st.session_state["page"] = "login"
                st.rerun()
            else:
                st.error(f"❌ Registration failed. Error: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Registration failed. Error: {e}")

elif st.session_state["page"] == "login":
    st.title("🔑 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            response = requests.post(f"{API_BASE_URL}login/", json={"email": email, "password": password})
            if response.status_code == 200:
                user_data = response.json()
                st.session_state["auth_token"] = user_data["token"]
                st.session_state["username"] = user_data["username"]
                st.session_state["page"] = "dashboard"
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error(f"❌ Invalid email or password. Error: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Login failed. Error: {e}")
