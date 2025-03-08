import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from utils import process_image, create_prompt, validate_dietary_restrictions
from auth import AuthManager

# Initialize authentication
auth = AuthManager()

# Configure page
try:
    st.set_page_config(page_title="Dietary Safety Checker",
                      page_icon="🍽️",
                      layout="centered")
except Exception as e:
    # In case set_page_config was already called
    pass

# Check authentication
if not auth.is_logged_in():
    st.warning("Please log in to use this application")
    st.stop()

# Load and apply custom CSS
css_loaded = False
try:
    if os.path.exists("assets/style.css"):
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            css_loaded = True
except Exception as e:
    st.warning("Custom styling could not be loaded. The app will still function normally.")

# Initialize Gemini API
try:
    GOOGLE_API_KEY = st.secrets.api_keys.GOOGLE_API_KEY
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    model_loaded = True
except Exception as e:
    st.error("Error initializing the AI model. Please check your API key configuration.")
    model_loaded = False

def analyze_product(image, dietary_restrictions):
    if not model_loaded:
        st.error("AI model not properly initialized")
        return None
    
    try:
        # Process image
        processed_img = process_image(image)
        # Create prompt
        prompt = create_prompt(dietary_restrictions)
        # Generate response from Gemini
        response = model.generate_content([prompt, processed_img])
        return response.text
    except Exception as e:
        st.error(f"An error occurred during analysis: {str(e)}")
        return None

def main():
    # Show user info and logout button in sidebar
    with st.sidebar:
        st.write(f"Logged in as: {auth.get_current_user()}")
        if st.button("Logout"):
            auth.logout()
            st.rerun()

    st.title("🍽️ Dietary Safety Checker")
    st.markdown("""
    Upload a photo of product ingredients and describe your dietary restrictions.
    We'll analyze if the product is safe for you to consume.
    """)

    # Image upload
    uploaded_file = st.file_uploader(
        "Upload ingredient list photo",
        type=["jpg", "jpeg", "png"],
        help="Take a clear photo of the ingredient list")

    # Dietary restrictions input
    dietary_restrictions = st.text_area(
        "Describe your dietary restrictions",
        placeholder="Example: I'm vegetarian and allergic to nuts",
        help="Include any allergies, religious restrictions, or dietary preferences"
    )

    if uploaded_file and dietary_restrictions:
        if st.button("Analyze Product", type="primary"):
            if not validate_dietary_restrictions(dietary_restrictions):
                st.warning("Please provide more detailed dietary restrictions")
                return

            with st.spinner("Analyzing ingredients..."):
                try:
                    # Display uploaded image
                    image = Image.open(uploaded_file)
                    st.image(image,
                            caption="Uploaded Ingredients",
                            use_container_width=True)

                    # Get analysis
                    analysis = analyze_product(image, dietary_restrictions)

                    if analysis:
                        st.markdown("### Analysis Results")
                        st.markdown(analysis)

                        # Add disclaimer
                        st.markdown("""
                        ---
                        **Disclaimer**: This analysis is AI-generated and should not be the sole basis
                        for dietary decisions. Always consult with healthcare professionals for medical advice.
                        """)
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.write("Please try refreshing the page.")
