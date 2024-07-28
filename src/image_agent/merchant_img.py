import enhance
from image_lab import ImageQualityChecker
import streamlit as st
import tempfile
import numpy as np
from PIL import Image
from ocr import extract_text, validate_image
from dotenv import load_dotenv
import os

load_dotenv()

IMG_PATH = os.getenv("IMG_PATH")

image_path = "test_image.jpg"
checker = ImageQualityChecker(image_path)
results = checker.check_quality()
print(results)


def main():
    st.title('Image Checker for Restaurant')

    resto_name = st.text_input('Enter restaurant name:')
    uploaded_file = st.file_uploader('Upload an image of the product:', type=['png', 'jpg', 'jpeg'])
    
    # default keywords for text validation
    default_keywords = ['sale', 'promo', 'grab', 'referensi', 'diskon', 'discount']
    keywords = st.text_area('Enter keywords for validation (comma-separated):', value=', '.join(default_keywords))
    keywords = [keyword.strip() for keyword in keywords.split(',')]

    if uploaded_file is not None and resto_name:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        
        image = Image.open(temp_file_path)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        quality_checker = ImageQualityChecker(temp_file_path)
        quality_results = quality_checker.check_quality()

        if quality_results['has_border']:
            st.warning('Image has a border. Please reupload an image without a border.')
        else:
            if quality_results['is_blurry']:
                st.info('Enhancing image due to blurriness.')
                enhanced_image =enhance.enhance_image(temp_file_path)
                st.image(enhanced_image, caption='Enhanced Image', use_column_width=True)
                enhanced_image.save(temp_file_path)
            
            extracted_text = extract_text(temp_file_path)
            st.write('Extracted Text:', extracted_text)

            status, message = validate_image(extracted_text, resto_name, keywords)
            if status == 'pass':
                st.success(message)
            else:
                st.error(message)

if __name__ == '__main__':
    main()