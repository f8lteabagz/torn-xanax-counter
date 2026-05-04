import os
import requests
from PIL import Image, ImageDraw, ImageFont

API_KEY = os.getenv("TORN_API_KEY")
BASE_IMAGE = "xans.jpg" 
OUTPUT_IMAGE = "xans_counter.jpg"

def get_xanax_count():
    url = f"https://api.torn.com/user/?selections=personalstats&key={API_KEY}"
    try:
        data = requests.get(url).json()
        return str(data.get('personalstats', {}).get('xantaken', 0))
    except:
        return "???"

def create_image():
    if not os.path.exists(BASE_IMAGE):
        print("Error: xans.jpg missing")
        return

    with Image.open(BASE_IMAGE) as img:
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        # Using a standard Linux font that supports 150pt size
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 150)
        except:
            font = ImageFont.load_default(size=150)

        text = f"JUNKIE: {get_xanax_count()}"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Neon Purple (191, 0, 255) with Black Outline
        draw.text(((w - tw) / 2, (h - th) / 2), text, fill=(191, 0, 255), 
                  font=font, stroke_width=5, stroke_fill=(0, 0, 0))
        
        img.save(OUTPUT_IMAGE)
        print("Success: Image created.")

if __name__ == "__main__":
    create_image()
    
