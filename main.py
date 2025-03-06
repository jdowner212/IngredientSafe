import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from utils import process_image, create_prompt, validate_dietary_restrictions

# Configure page
st.set_page_config(page_title="Dietary Safety Checker",
                   page_icon="🍽️",
                   layout="centered")

# Load and apply custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Gemini API
# my_secret = os.environ['gemini_api_key']
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", my_secret)
# GOOGLE_API_KEY = os.getenv('gemini_api_key')
GOOGLE_API_KEY = 'AIzaSyCKvYUBDy6LBKevePp9RdniBqMIMmVIB5U'

print('GOOGLE_API_KEY:', GOOGLE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel('gemini-pro-vision')
model = genai.GenerativeModel('gemini-1.5-flash')


def analyze_product(image, dietary_restrictions):
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
        help=
        "Include any allergies, religious restrictions, or dietary preferences"
    )

    if uploaded_file and dietary_restrictions:
        if st.button("Analyze Product", type="primary"):
            if not validate_dietary_restrictions(dietary_restrictions):
                st.warning("Please provide more detailed dietary restrictions")
                return

            with st.spinner("Analyzing ingredients..."):
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


if __name__ == "__main__":
    main()
