import pytesseract

def extract_text(image):
    text = pytesseract.image_to_string(image)
    return text

def validate_image(text, resto_name, keywords):
    if any(keyword in text.lower() for keyword in keywords):
        return 'pass', 'Image passed the check.'
    elif resto_name.lower() not in text.lower():
        return 'fail', 'Image text does not match the restaurant name. It might be a fake or stolen photo.'
    return 'pass', 'Image passed the check.'