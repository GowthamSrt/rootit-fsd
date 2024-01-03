import streamlit as st

def signup():
    st.subheader("Sign Up")

    username = st.text_input("Username / email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password == confirm_password:
            st.success(f"Welcome, {username}! You have successfully signed up.")
        else:
            st.error("Passwords do not match. Please try again.")

def login():
    st.subheader("Log In")

    username = st.text_input("Username / email")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        # Perform authentication (for simplicity, we assume a hardcoded user)
        if username == "demo" and password == "demo123":
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Authentication failed. Please check your credentials.")

def main():
    st.title("User Authentication System")

    # Set background image
    st.markdown(
        """
        <style>
            body {
                background-image: url("p-2/assets/1.jpg");
                background-size: cover;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.write("Welcome to the User Authentication System.")
    st.button("Sign Up", on_click=signup)
    st.button("Log In", on_click=login)

if __name__ == "__main__":
    main()
