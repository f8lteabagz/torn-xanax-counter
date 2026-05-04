import os
import requests
from PIL import Image, ImageDraw, ImageFont

# Grabs your secret API key
API_KEY = os.getenv("TORN_API_KEY")
BASE_IMAGE = "xans.jpg" 
OUTPUT_IMAGE = "xans_counter.jpg"

def get_xanax_count():
    url = f"https://api.torn.com/user/?selections=personalstats&key={API_KEY}"
    try:
        data = requests.get(url).json()
        if 'error' in data:
            return "ERR"
        return str(data.get('personalstats', {}).get('xantaken', 0))
    except:
        return "???"

def create_image():
    if not os.path.exists(BASE_IMAGE):
        print("Error: xans.jpg not found!")
        return

    with Image.open(BASE_IMAGE) as img:
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        # This is the fail-proof font part
        try:
            # Try the most common Linux font path first
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 400)
        except:
            # If that fails, Pillow 10+ allows scaling the default font like this
            try:
                font = ImageFont.load_default(size=400)
            except:
                font = ImageFont.load_default()

        text = f"JUNKIE: {get_xanax_count()}"
        
        # Centering Math
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        # Neon Purple (191, 0, 255) with Black Outline
        draw.text(((w - tw) / 2, (h - th) / 2), text, fill=(191, 0, 255), 
                  font=font, stroke_width=10, stroke_fill=(0, 0, 0))
        
        img.save(OUTPUT_IMAGE)
        print(f"Success: Created xans_counter.jpg with count {text}")

if __name__ == "__main__":
    create_image()
    
