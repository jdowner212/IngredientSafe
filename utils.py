from PIL import Image
import io

def process_image(image):
    """
    Process the uploaded image for Gemini API
    """
    # Ensure image is in RGB format
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Resize if too large (Gemini has limits)
    max_size = 1600
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = tuple(int(dim * ratio) for dim in image.size)
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    return image

def create_prompt(dietary_restrictions):
    """
    Create a structured prompt for Gemini API
    """
    return f"""
    Analyze the ingredients shown in this image and determine if the product is safe for someone with the following dietary restrictions:
    {dietary_restrictions}

    Please provide:
    1. Whether the product is safe or unsafe
    2. A detailed explanation of your analysis
    3. Any concerning ingredients if present
    4. Suggested alternatives if the product is unsafe

    Format your response in a clear, easy-to-read manner.
    """

def validate_dietary_restrictions(restrictions):
    """
    Validate that dietary restrictions are sufficiently detailed
    """
    # Check minimum length
    if len(restrictions.strip()) < 10:
        return False
    
    # Check for common dietary terms
    common_terms = ['vegetarian', 'vegan', 'allerg', 'gluten', 'dairy', 'kosher', 'halal', 
                   'nut', 'egg', 'soy', 'fish', 'shellfish', 'wheat', 'lactose']
    
    return any(term in restrictions.lower() for term in common_terms)
