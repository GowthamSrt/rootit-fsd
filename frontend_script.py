# frontend/app.py

import streamlit as st
import requests
import json  # Added import for JSONDecodeError

# Backend API base URL
BASE_URL = "http://localhost:5000/api"  # Update with your Flask backend URL

# Authentication token (you might handle this differently in a real-world scenario)
TOKEN = ""

# Functions to interact with the backend
def authenticate_user(email, password):
    url = f"{BASE_URL}/auth/login"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)

    # Updated to handle non-JSON responses
    try:
        return response.json()
    except json.JSONDecodeError:
        print(f"Non-JSON response: {response.content}")
        return {"message": "Error processing response"}

def register_user(first_name, last_name, email, password, dob):
    url = f"{BASE_URL}/auth/register"
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "dob": dob,
    }
    response = requests.post(url, json=data)

    # Updated to handle non-JSON responses
    if response.status_code != 200:
        print(f"Non-200 status code: {response.status_code}")
        print(f"Response content: {response.content}")
        return {"message": "Error processing response"}

    try:
        return response.json()
    except json.JSONDecodeError:
        print(f"Non-JSON response: {response.content}")
        return {"message": "Error processing response"}

# Streamlit UI
def login_page():
    st.title("Login")
    login_email = st.text_input("Email")
    login_password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_email and login_password:
            auth_result = authenticate_user(login_email, login_password)
            if "token" in auth_result:
                TOKEN = auth_result["token"]
                st.success("Logged in successfully!")
            else:
                st.error("Login failed. Please check your credentials.")
        else:
            st.warning("Email and password are mandatory fields.")

def register_page():
    st.title("Register")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    register_email = st.text_input("Email")
    register_password = st.text_input("Password", type="password")
    dob = st.date_input("Date of Birth")
    if st.button("Register"):
        if first_name and last_name and register_email and register_password and dob:
            register_result = register_user(
                first_name, last_name, register_email, register_password, str(dob)
            )
            if "token" in register_result:
                TOKEN = register_result["token"]
                st.success("Registered and logged in successfully!")
            else:
                st.error(f"Registration failed. Server message: {register_result.get('message', 'Unknown error')}")
        else:
            st.warning("All fields are mandatory.")

def authenticate_user(email, password):
    url = f"{BASE_URL}/auth/login"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)

    # Handle non-JSON responses
    if response.status_code != 200:
        print(f"Non-200 status code: {response.status_code}")
        print(f"Response content: {response.content}")
        return {"message": "Error processing response"}

    try:
        return response.json()
    except json.JSONDecodeError:
        print(f"Non-JSON response: {response.content}")
        return {"message": "Error processing response"}


def main():
    st.title("Streamlit Frontend with Flask Backend")

    # Page navigation buttons
    page = st.radio("Navigation", ["Login", "Register"])
    if page == "Login":
        login_page()
    elif page == "Register":
        register_page()

if __name__ == "__main__":
    main()
