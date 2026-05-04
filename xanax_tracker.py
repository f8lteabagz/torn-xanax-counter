import os
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# 1. Load the secret API key
load_dotenv()
API_KEY = os.getenv('TORN_API_KEY')

def get_xanax_count():
    url = f"https://api.torn.com/user/?selections=personalstats&key={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return str(data.get('personalstats', {}).get('xantaken', 0))
    except:
        return "N/A"

def create_image(count):
    img_path = "xans.jpg"
    if not os.path.exists(img_path):
        print("xans.jpg not found!")
        return

    with Image.open(img_path) as img:
        draw = ImageDraw.Draw(img)
        # Using default font for compatibility
        font = ImageFont.load_default()
        
        # Position (X, Y) and Color (Neon Green)
        draw.text((50, 50), f"Xanax Taken: {count}", fill=(57, 255, 20), font=font)
        
        img.save("xans_counter.jpg")
        print("Updated image saved as xans_counter.jpg")

if __name__ == "__main__":
    count = get_xanax_count()
    create_image(count)
