import streamlit as st
import hashlib
import requests
from typing import Optional

class AuthManager:
    def __init__(self):
        # Try to get Mailchimp credentials, with better error handling
        try:
            self.mailchimp_api_key = st.secrets.mailchimp.MAILCHIMP_API_KEY
            self.mailchimp_list_id = st.secrets.mailchimp.MAILCHIMP_LIST_ID
            self.mailchimp_server = st.secrets.mailchimp.MAILCHIMP_SERVER
            
            # Extract server prefix from API key if not specified
            if not self.mailchimp_server and "-" in self.mailchimp_api_key:
                self.mailchimp_server = self.mailchimp_api_key.split("-")[-1]
            
            self.mailchimp_configured = all([
                self.mailchimp_api_key,
                self.mailchimp_list_id,
                self.mailchimp_server
            ])
        except Exception as e:
            st.warning("Mailchimp integration is not configured. Some features may be limited.")
            self.mailchimp_configured = False
            self.mailchimp_api_key = ""
            self.mailchimp_list_id = ""
            self.mailchimp_server = ""

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def subscribe_to_mailchimp(self, email: str, first_name: str, last_name: str) -> bool:
        if not self.mailchimp_configured:
            st.warning("Mailchimp integration is not configured. Proceeding with signup without newsletter subscription.")
            return True

        url = f"https://{self.mailchimp_server}.api.mailchimp.com/3.0/lists/{self.mailchimp_list_id}/members"
        data = {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": first_name,
                "LNAME": last_name
            }
        }
        auth = ("anystring", self.mailchimp_api_key)
        
        try:
            response = requests.post(url, json=data, auth=auth)
            if response.status_code == 200:
                st.success("Successfully subscribed to newsletter!")
                return True
            else:
                error_detail = response.json().get('detail', 'Unknown error')
                if "already a list member" in error_detail.lower():
                    st.info("Email already subscribed to newsletter. Proceeding with signup.")
                    return True
                st.error(f"Failed to subscribe to newsletter: {error_detail}")
                return False
        except Exception as e:
            st.error(f"Error subscribing to newsletter: {str(e)}")
            return False

    def signup(self, email: str, password: str, first_name: str, last_name: str) -> bool:
        if 'users' not in st.session_state:
            st.session_state.users = {}

        if email in st.session_state.users:
            st.error("Email already registered")
            return False

        # Try to subscribe to Mailchimp, but don't block signup if it fails
        mailchimp_result = self.subscribe_to_mailchimp(email, first_name, last_name)
        
        # Store user data (in a real app, use a database)
        st.session_state.users[email] = {
            'password': self._hash_password(password),
            'first_name': first_name,
            'last_name': last_name
        }
        return True

    def login(self, email: str, password: str) -> bool:
        if 'users' not in st.session_state:
            st.session_state.users = {}

        if email not in st.session_state.users:
            st.error("Email not registered")
            return False

        if st.session_state.users[email]['password'] == self._hash_password(password):
            st.session_state.user = email
            return True
        
        st.error("Invalid password")
        return False

    def logout(self):
        if 'user' in st.session_state:
            del st.session_state.user

    def is_logged_in(self) -> bool:
        return 'user' in st.session_state

    def get_current_user(self) -> Optional[str]:
        return st.session_state.get('user') 