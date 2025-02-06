import streamlit as st
import requests

st.set_page_config(page_title="Register", layout="wide")

# Backend API URL for registration
API_REGISTER_URL = "https://finalproject-production-171c.up.railway.app/api/users/register/"

st.title("Register")
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
role = st.selectbox("Role", ["student", "professor"])

# Registration Function
def register_user(username, email, password, role):
    response = requests.post(API_REGISTER_URL, json={
        "username": username,
        "email": email,
        "password": password,
        "role": role
    })
    return response.status_code == 201  # True if successful

if st.button("Register"):
    if register_user(username, email, password, role):
        st.success("Registration successful! Please login.")
        st.switch_page("pages/login.py")
    else:
        st.error("Registration failed. Try again.")
