import streamlit as st
import requests
import subprocess

# Start the Flask backend in a separate process
backend_process = subprocess.Popen(["python", "backend_script.py"])

# Wait for the backend to start (you may need to adjust the waiting time)
import time
time.sleep(3)

BASE_URL = "http://localhost:5000/api"

# Define a class to store session state
class SessionState:
    def __init__(self):
        self.access_token = None

# Create a session state object
st.session_state = SessionState()

def register():
    st.subheader("User Registration")

    username = st.text_input("Username", key="register_username_input")
    password = st.text_input("Password", type="password", key="register_password_input")

    if st.button("Register"):
        response = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})
        st.write(response.json().get('message'))

def login():
    st.subheader("User Login")

    username = st.text_input("Username", key="login_username_input")
    password = st.text_input("Password", type="password", key="login_password_input")

    if st.button("Login"):
        response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.write("Login successful")
            # Store the access token for further API calls
            st.session_state.access_token = response.json().get('access_token')
        else:
            st.write("Login failed. Invalid credentials.")

def get_tasks():
    st.subheader("User Tasks")

    if st.session_state.access_token:
        response = requests.get(f"{BASE_URL}/tasks", headers={"Authorization": f"Bearer {st.session_state.access_token}"})
        if response.status_code == 200:
            tasks = response.json()
            st.write(tasks)
        else:
            st.write("Failed to retrieve tasks.")
    else:
        st.write("Please log in to view tasks.")

def main():
    st.title("Task Manager App")

    register()
    login()
    get_tasks()

if __name__ == '__main__':
    main()

# Terminate the backend process when Streamlit app is closed
backend_process.terminate()
