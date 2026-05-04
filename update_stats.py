import os
import requests
from PIL import Image, ImageDraw, ImageFont

# Grabs your secret API key from GitHub Secrets
API_KEY = os.getenv("TORN_API_KEY")
BASE_IMAGE = "xans.jpg" 
OUTPUT_IMAGE = "xans_counter.jpg"

def get_xanax_count():
    url = f"https://api.torn.com/user/?selections=personalstats&key={API_KEY}"
    try:
        data = requests.get(url).json()
        # If API is down or key is wrong, show '???' instead of crashing
        if 'error' in data:
            return "???"
        return str(data.get('personalstats', {}).get('xantaken', 0))
    except:
        return "???"

def create_image():
    if not os.path.exists(BASE_IMAGE):
        print("Error: xans.jpg not found in repository!")
        return

    with Image.open(BASE_IMAGE) as img:
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        # LOCKED FONT SIZE: 150
        try:
            # Standard Linux font path for GitHub servers
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 150)
        except:
            # Fallback if the specific font file isn't found
            try:
                font = ImageFont.load_default(size=150)
            except:
                font = ImageFont.load_default()

        text = f"JUNKIE: {get_xanax_count()}"
        
        # Centering Logic
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        # Neon Purple (191, 0, 255) with Black Outline (stroke)
        # Stroke width 5 looks good with font size 150
        draw.text(((w - tw) / 2, (h - th) / 2), text, fill=(191, 0, 255), 
                  font=font, stroke_width=5, stroke_fill=(0, 0, 0))
        
        img.save(OUTPUT_IMAGE)
        print(f"Success: Created xans_counter.jpg with Font Size 150")

if __name__ == "__main__":
    create_image()
    
