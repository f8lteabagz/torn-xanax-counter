import os, requests
from PIL import Image, ImageDraw, ImageFont

def get_count():
    try:
        r = requests.get(f"https://api.torn.com/user/?selections=personalstats&key={os.getenv('TORN_API_KEY')}")
        return str(r.json().get('personalstats', {}).get('xantaken', 0))
    except: return "???"

if os.path.exists("xans.jpg"):
    with Image.open("xans.jpg") as img:
        draw = ImageDraw.Draw(img)
        try:
            f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 150)
        except:
            f = ImageFont.load_default(size=150)
        
        txt = f"JUNKIE: {get_count()}"
        bbox = draw.textbbox((0, 0), txt, font=f)
        draw.text(((img.size[0]-(bbox[2]-bbox[0]))/2, (img.size[1]-(bbox[3]-bbox[1]))/2), txt, fill=(191,0,255), font=f, stroke_width=5, stroke_fill=(0,0,0))
        img.save("xans_counter.jpg")
else:
    print("Error: xans.jpg not found")
    
