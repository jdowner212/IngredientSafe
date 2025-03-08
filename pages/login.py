import streamlit as st
from auth import AuthManager

st.set_page_config(page_title="Login - Dietary Safety Checker", page_icon="🔒")

# Initialize authentication manager
auth = AuthManager()

def show_login():
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if auth.login(email, password):
                st.success("Successfully logged in!")
                st.rerun()

def show_signup():
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submitted = st.form_submit_button("Sign Up")
        
        if submitted:
            if password != confirm_password:
                st.error("Passwords don't match")
                return
            
            if auth.signup(email, password, first_name, last_name):
                st.success("Successfully signed up! Please log in.")
                st.session_state.show_signup = False
                st.rerun()

def main():
    if auth.is_logged_in():
        st.write(f"Welcome back, {auth.get_current_user()}!")
        if st.button("Logout"):
            auth.logout()
            st.rerun()
        return

    # Initialize session state
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False

    # Toggle between login and signup
    if not st.session_state.show_signup:
        st.title("Login")
        show_login()
        if st.button("Don't have an account? Sign up"):
            st.session_state.show_signup = True
            st.rerun()
    else:
        st.title("Sign Up")
        show_signup()
        if st.button("Already have an account? Log in"):
            st.session_state.show_signup = False
            st.rerun()

if __name__ == "__main__":
    main() 