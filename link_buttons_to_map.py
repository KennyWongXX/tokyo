import re
import json

# Data from subagent
locations_data = {
  "Mutekiya Ramen (Ikebukuro)": { "lat": 35.7279, "lng": 139.7113, "region": "tokyo" },
  "Torikizoku (Ikebukuro East Exit)": { "lat": 35.7305, "lng": 139.7125, "region": "tokyo" },
  "Hungry Bear Curry (Tokyo Disneyland)": { "lat": 35.6331, "lng": 139.8805, "region": "tokyo" },
  "Queen of Hearts Banquet Hall (Tokyo Disneyland)": { "lat": 35.6318, "lng": 139.8813, "region": "tokyo" },
  "Vulcania Restaurant (Tokyo DisneySea)": { "lat": 35.6267, "lng": 139.8850, "region": "tokyo" },
  "Sebastian's Calypso Kitchen (Tokyo DisneySea)": { "lat": 35.6264, "lng": 139.8835, "region": "tokyo" },
  "Ekibenya Matsuri (Tokyo Station)": { "lat": 35.6812, "lng": 139.7671, "region": "tokyo" },
  "Maidreamin Akihabara (Main Store)": { "lat": 35.6984, "lng": 139.7712, "region": "tokyo" },
  "Gyukatsu Motomura (Akihabara)": { "lat": 35.6978, "lng": 139.7725, "region": "tokyo" },
  "PABLO Mini (Akihabara)": { "lat": 35.6982, "lng": 139.7728, "region": "tokyo" },
  "Bills (Omotesando)": { "lat": 35.6694, "lng": 139.7060, "region": "tokyo" },
  "AFURI (Harajuku)": { "lat": 35.6716, "lng": 139.7031, "region": "tokyo" },
  "Uobei Sushi (Shibuya Dogenzaka)": { "lat": 35.6595, "lng": 139.6985, "region": "tokyo" },
  "Houtou Fudou (Kawaguchiko Station / near FujiQ)": { "lat": 35.4977, "lng": 138.7695, "region": "tokyo" },
  "CoCo Ichibanya (Kawaguchiko)": { "lat": 35.5010, "lng": 138.7630, "region": "tokyo" },
  "Kinryu Ramen (Dotonbori)": { "lat": 34.6687, "lng": 135.5038, "region": "osaka" },
  "Kani Doraku (Dotonbori Honten)": { "lat": 34.6687, "lng": 135.5033, "region": "osaka" },
  "Mizuno Okonomiyaki (Dotonbori)": { "lat": 34.6685, "lng": 135.5035, "region": "osaka" },
  "Acchichi Honpo (Dotonbori)": { "lat": 34.6690, "lng": 135.5036, "region": "osaka" },
  "Three Broomsticks (USJ)": { "lat": 34.6654, "lng": 135.4323, "region": "osaka" },
  "Kinopio's Cafe (USJ)": { "lat": 34.6654, "lng": 135.4323, "region": "osaka" },
  "551 Horai (Namba)": { "lat": 34.6655, "lng": 135.5015, "region": "osaka" },
  "Takeru (Nipponbashi)": { "lat": 34.6625, "lng": 135.5055, "region": "osaka" },
  "Kushikatsu Daruma (Shinsekai)": { "lat": 34.6520, "lng": 135.5066, "region": "osaka" },
  "Super Tamade (Nipponbashi)": { "lat": 34.6665, "lng": 135.5075, "region": "osaka" },
  "Kura Sushi (Expocity)": { "lat": 34.8055, "lng": 135.5320, "region": "osaka" },
  "Yakiniku Rikimaru (Namba)": { "lat": 34.6650, "lng": 135.5010, "region": "osaka" },
  "Rikuro Ojisan (Namba)": { "lat": 34.6655, "lng": 135.5015, "region": "osaka" },
  "Endo Sushi (Osaka Central Fish Market)": { "lat": 34.6850, "lng": 135.4830, "region": "osaka" },
  "Kansai Airport (KIX)": { "lat": 34.4320, "lng": 135.2304, "region": "osaka" }
}

# Mapping from HTML keywords to Data Keys
# This is manual mapping based on the HTML content I know
key_map = {
    "Mutekiya": "Mutekiya Ramen (Ikebukuro)",
    "Torikizoku": "Torikizoku (Ikebukuro East Exit)",
    "Konbini": "Mutekiya Ramen (Ikebukuro)", # Fallback to Ikebukuro area
    "Hungry Bear Curry": "Hungry Bear Curry (Tokyo Disneyland)",
    "Queen of Hearts": "Queen of Hearts Banquet Hall (Tokyo Disneyland)",
    "Vulcania": "Vulcania Restaurant (Tokyo DisneySea)",
    "Sebastian": "Sebastian's Calypso Kitchen (Tokyo DisneySea)",
    "Ekiben": "Ekibenya Matsuri (Tokyo Station)",
    "Maidreamin": "Maidreamin Akihabara (Main Store)",
    "Gyukatsu": "Gyukatsu Motomura (Akihabara)",
    "PABLO": "PABLO Mini (Akihabara)",
    "Bills": "Bills (Omotesando)",
    "AFURI": "AFURI (Harajuku)",
    "Uobei": "Uobei Sushi (Shibuya Dogenzaka)",
    "Hoto": "Houtou Fudou (Kawaguchiko Station / near FujiQ)",
    "CoCo": "CoCo Ichibanya (Kawaguchiko)",
    "Kinryu": "Kinryu Ramen (Dotonbori)",
    "Kani": "Kani Doraku (Dotonbori Honten)",
    "Mizuno": "Mizuno Okonomiyaki (Dotonbori)",
    "Acchichi": "Acchichi Honpo (Dotonbori)",
    "Three Broomsticks": "Three Broomsticks (USJ)",
    "Kinopio": "Kinopio's Cafe (USJ)",
    "551": "551 Horai (Namba)",
    "Takeru": "Takeru (Nipponbashi)",
    "Daruma": "Kushikatsu Daruma (Shinsekai)",
    "Tamade": "Super Tamade (Nipponbashi)",
    "Kura": "Kura Sushi (Expocity)",
    "Rikimaru": "Yakiniku Rikimaru (Namba)",
    "Rikuro": "Rikuro Ojisan (Namba)",
    "Endo": "Endo Sushi (Osaka Central Fish Market)",
    "Airport": "Kansai Airport (KIX)"
}

file_path = r"c:\Python\code\東京\Japan_Trip_Plan_Final_v10.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update JS Arrays
# We need to inject these new locations into the JS arrays at the bottom
# Find "var tokyoLocations = [" and "var osakaLocations = ["

new_tokyo_locs = []
new_osaka_locs = []

for key, data in locations_data.items():
    entry = f'        {{ name: "{key}", lat: {data["lat"]}, lng: {data["lng"]} }}'
    if data["region"] == "tokyo":
        new_tokyo_locs.append(entry)
    else:
        new_osaka_locs.append(entry)

# Insert into Tokyo
tokyo_insert = ",\n".join(new_tokyo_locs)
content = re.sub(r'(var tokyoLocations = \[\s*)', r'\1' + tokyo_insert + ",\n", content)

# Insert into Osaka
osaka_insert = ",\n".join(new_osaka_locs)
content = re.sub(r'(var osakaLocations = \[\s*)', r'\1' + osaka_insert + ",\n", content)


# 2. Update Buttons
# Find the buttons we added: <a href="..." target="_blank" class="food-map-link">📍</a>
# We need to match them with the food item preceding them to know which location to use.

# Pattern:
# <a href="...food-item"> ... Name ... </a>
# <a href="...food-map-link">📍</a>

# We will iterate through the content and replace the map links.
# Since regex replacement with context is tricky, we'll use a function.

def replace_map_link(match):
    # match.group(1) is the food item link and name
    # match.group(2) is the map link
    
    food_part = match.group(1)
    
    # Identify the key from the food part
    found_key = None
    found_name = "Unknown"
    
    # Try to match keys from our map
    for key in key_map:
        if key in food_part:
            found_key = key
            break
            
    if not found_key:
        # Fallback: try to find any known name in the text
        # This is a bit loose but should work for most
        pass

    if found_key:
        full_name = key_map[found_key]
        data = locations_data[full_name]
        lat = data["lat"]
        lng = data["lng"]
        region = data["region"]
        
        new_link = f'<a href="javascript:void(0)" onclick="focusMap({lat}, {lng}, \'{region}\')" class="food-map-link">📍</a>'
        return food_part + "\n            " + new_link
    else:
        # If we can't identify it, leave it as a google search link (or maybe just leave it alone)
        # But the user wants "use the above map".
        # Let's try to default to a region center if unknown? No, better to leave as search if unknown.
        return match.group(0)

# Regex to capture the pair
# We look for the food item </a> followed by whitespace and the map link
pattern = re.compile(r'(<a href="[^"]+" target="_blank" class="food-item">.*?</a>)\s*<a href="[^"]+" target="_blank" class="food-map-link">📍</a>', re.DOTALL)

new_content = pattern.sub(replace_map_link, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated map locations and buttons.")
