import streamlit as st
import requests

st.set_page_config(page_title="Login", layout="wide")

# Backend API URL for Login
API_LOGIN_URL = "https://finalproject-production-171c.up.railway.app/api/users/login/"

st.title("Login")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# Login Function
def login_user(email, password):
    response = requests.post(API_LOGIN_URL, json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json()  # Returns {'token': '...', 'username': '...'}
    return None

if st.button("Login"):
    user_data = login_user(email, password)
    if user_data:
        st.session_state["auth_token"] = user_data["token"]
        st.session_state["username"] = user_data["username"]
        st.success("Login successful! Redirecting...")
        st.switch_page("pages/dashboard.py")
    else:
        st.error("Invalid email or password. Please try again.")
