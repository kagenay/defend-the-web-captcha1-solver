import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import io
import time
import os

DEBUG_DIR = "captcha_debug"
os.makedirs(DEBUG_DIR, exist_ok=True)

def debug_save_image(image, name):
    path = os.path.join(DEBUG_DIR, f"{name}_{int(time.time())}.png")
    image.save(path)
    print(f"Saved debug image: {path}")
    return path

def extract_text(image):
    configs = [
         r'--oem 3 --psm 6 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()-_=+<>?"'
    ]
    
    for cfg in configs:
        text = pytesseract.image_to_string(image, config=cfg).strip()
        if text:
            return text
    

    return ""

# Configure your cookies here
cookies_dict = {
    "cookies_dismissed": "",
    "PHPSESSID": "",
    "__rum_sid": ""
}

# Initialize session with cookies
session = requests.Session()
session.cookies.update(cookies_dict)

# Get challenge page
try:
    response = session.get("https://defendtheweb.net/playground/captcha1")
    response.raise_for_status()
except Exception as e:
    print(f"Failed to get challenge page: {str(e)}")
    exit()

# Parse form data
try:
    soup = BeautifulSoup(response.content, 'html.parser')
    form = soup.find('form', {'class': 'form--captcha-1'})
    token = form.find('input', {'name': 'token'})['value']
    formid = form.find('input', {'name': 'formid'})['value']
except Exception as e:
    print(f"Failed to parse form data: {str(e)}")
    exit()

# Download CAPTCHA image
try:
    image_response = session.get("https://defendtheweb.net/extras/playground/captcha/captcha1.php")
    original_image = Image.open(io.BytesIO(image_response.content))
except Exception as e:
    print(f"Failed to download CAPTCHA image: {str(e)}")
    exit()

debug_save_image(original_image, "original")

# OCR extraction
captcha_text = extract_text(original_image)
reversed_captcha = captcha_text[::-1]

print("\n=== DEBUG INFO ===")
print(f"Raw OCR Output: {repr(captcha_text)}")
print(f"Reversed CAPTCHA: {repr(reversed_captcha)}")
print(f"Text Length: {len(captcha_text)} characters")

if not captcha_text:
    print("\nERROR: No text detected in CAPTCHA image!")
    exit()

# Submit answer
try:
    response = session.post(
        "https://defendtheweb.net/playground/captcha1",
        data={'token': token, 'formid': formid, 'answer': reversed_captcha},
        timeout=5
    )
    response.raise_for_status()
except Exception as e:
    print(f"\nSubmission failed: {str(e)}")
    exit()

# Analyze results
print("\n=== SERVER RESPONSE ===")
if "level expired" in response.text:
    print("Result: Time expired")
elif "Invalid login details" in response.text:
    print("Result: Incorrect CAPTCHA")
else:
    print("Result: Success!")

# Save response
with open(os.path.join(DEBUG_DIR, f"response_{int(time.time())}.html"), "w", encoding="utf-8") as f:
    f.write(response.text)
