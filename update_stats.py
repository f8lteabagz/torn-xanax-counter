import os, requests
from PIL import Image, ImageDraw, ImageFont

def get_count():
    api_key = os.getenv('TORN_API_KEY')
    
    # Check if the secret is missing or empty
    if not api_key:
        print("ERROR: TORN_API_KEY is missing or empty!")
        return "NO_KEY"
        
    try:
        r = requests.get(f"https://api.torn.com/user/?selections=personalstats&key={api_key}")
        data = r.json()
        
        # If Torn rejects the request, print the exact reason to the log
        if 'error' in data:
            print(f"TORN API ERROR: {data['error']}")
            return "API_ERR"
            
        stats = data.get('personalstats', {})
        
        # Grab the Xanax count
        if 'xantaken' in stats:
            print(f"Success! Found {stats['xantaken']} Xanax taken.")
            return str(stats['xantaken'])
        else:
            print("Error: 'xantaken' was not in the API response.")
            return "0"
            
    except Exception as e: 
        print(f"Request failed: {e}")
        return "???"

if os.path.exists("xans.jpg"):
    with Image.open("xans.jpg") as img:
        draw = ImageDraw.Draw(img)
        
        try:
            f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 150)
        except:
            f = ImageFont.load_default(size=150)
        
        txt = f"JUNKIE: {get_count()}"
        
        # Fixed coordinate math to perfectly center the text
        bbox = draw.textbbox((0, 0), txt, font=f)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (img.size[0] - text_width) / 2 - bbox[0]
        y = (img.size[1] - text_height) / 2 - bbox[1]
        
        draw.text((x, y), txt, fill=(191,0,255), font=f, stroke_width=5, stroke_fill=(0,0,0))
        img.save("xans_counter.jpg")
        print("Image updated successfully!")
else:
    print("Error: xans.jpg not found")
    
