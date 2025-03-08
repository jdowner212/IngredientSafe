import streamlit as st
from auth import AuthManager

st.set_page_config(
    page_title="Login - GroceryHelper AI",
    page_icon="🛒",
    initial_sidebar_state="collapsed"
)

# Initialize authentication manager
auth = AuthManager()

# Add custom CSS for better styling
st.markdown("""
<style>
    .welcome-text {
        text-align: center;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def show_welcome_message():
    st.markdown("""
    <div class="welcome-text">
        <h2>Welcome to GroceryHelper AI! 🛒</h2>
        <p>Your intelligent assistant for making safe and informed food choices.</p>
    </div>
    """, unsafe_allow_html=True)

def show_login():
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        col1, col2 = st.columns([1, 1])
        with col1:
            submitted = st.form_submit_button("Login", use_container_width=True)
        with col2:
            signup_redirect = st.form_submit_button("Need an account?", use_container_width=True)
        
        if submitted and email and password:
            if auth.login(email, password):
                st.success("Successfully logged in!")
                st.rerun()
        elif signup_redirect:
            st.session_state.show_signup = True
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
        
        col3, col4 = st.columns([1, 1])
        with col3:
            submitted = st.form_submit_button("Sign Up", use_container_width=True)
        with col4:
            login_redirect = st.form_submit_button("Already have an account?", use_container_width=True)
        
        if submitted and all([email, password, confirm_password, first_name, last_name]):
            if password != confirm_password:
                st.error("Passwords don't match")
                return
            
            if auth.signup(email, password, first_name, last_name):
                st.success("Successfully signed up! Please log in.")
                st.session_state.show_signup = False
                st.rerun()
        elif login_redirect:
            st.session_state.show_signup = False
            st.rerun()

def main():
    if auth.is_logged_in():
        st.write(f"Welcome back, {auth.get_current_user()}!")
        if st.button("Go to App", type="primary"):
            st.switch_page("main.py")
        if st.button("Logout"):
            auth.logout()
            st.rerun()
        return

    # Show welcome message
    show_welcome_message()

    # Initialize session state
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False

    # Check if coming from Mailchimp using the new query_params
    if 'from' in st.query_params and st.query_params['from'] == 'mailchimp':
        st.info("Welcome from our newsletter! Please sign up or log in to continue.")

    # Toggle between login and signup
    if not st.session_state.show_signup:
        show_login()
    else:
        show_signup()

if __name__ == "__main__":
    main() 