# streamlit_app.py
import streamlit as st
import requests

# Set your server address
SERVER_ADDRESS = "http://localhost:5000"

# Streamlit UI for user registration and login
st.title("Task Management App")

# User Registration
st.header("User Registration")
reg_username = st.text_input("Username:")
reg_password = st.text_input("Password:", type="password")
reg_button = st.button("Register")

if reg_button:
    # Make a POST request to register a new user
    response = requests.post(f"{SERVER_ADDRESS}/api/register", json={"username": reg_username, "password": reg_password})

    if response.status_code == 201:
        st.success("Registration successful! You can now log in.")
    else:
        st.error(f"Registration failed. Error: {response.json().get('error')}")

# User Login
st.header("User Login")
login_username = st.text_input("Username:")
login_password = st.text_input("Password:", type="password")
login_button = st.button("Login")

if login_button:
    # Make a POST request to log in
    response = requests.post(f"{SERVER_ADDRESS}/api/login", json={"username": login_username, "password": login_password})

    if response.status_code == 200:
        user_data = response.json().get('user')
        st.success(f"Login successful! Welcome, {user_data['username']}.")

        # Save user data for future requests
        st.session_state.user_data = user_data
    else:
        st.error(f"Login failed. Error: {response.json().get('error')}")

# Streamlit UI for dashboard and CRUD operations
if hasattr(st.session_state, 'user_data'):
    st.header("Task Dashboard")

    # CRUD Operations
    task_description = st.text_input("Task Description:")
    add_task_button = st.button("Add Task")

    if add_task_button:
        # Make a POST request to create a new task
        response = requests.post(f"{SERVER_ADDRESS}/api/tasks", json={"description": task_description})

        if response.status_code == 201:
            st.success("Task created successfully!")
        else:
            st.error(f"Failed to create task. Error: {response.json().get('error')}")

    # Display tasks
    st.subheader("Task List")

    # Make a GET request to retrieve tasks
    response = requests.get(f"{SERVER_ADDRESS}/api/tasks")

    if response.status_code == 200:
        tasks = response.json().get('tasks')
        for i, task in enumerate(tasks):
            st.write(f"{i + 1}. {task['description']}")

    else:
        st.error(f"Failed to retrieve tasks. Error: {response.json().get('error')}")
