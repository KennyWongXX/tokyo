import re
import json

# Coordinates data
food_locations = {
  "Torikizoku": { "lat": 35.7308, "lng": 139.7128, "region": "tokyo" },
  "Alice": { "lat": 35.6925, "lng": 139.7015, "region": "tokyo" }, # Generic Alice
  "Mutekiya": { "lat": 35.7278, "lng": 139.7115, "region": "tokyo" },
  "Ichiran": { "lat": 35.7321, "lng": 139.7125, "region": "tokyo" },
  "Vulcania": { "lat": 35.6267, "lng": 139.8850, "region": "tokyo" },
  "Sebastian": { "lat": 35.6247, "lng": 139.8819, "region": "tokyo" },
  "Maid Cafe": { "lat": 35.6983, "lng": 139.7710, "region": "tokyo" },
  "PABLO": { "lat": 35.6980, "lng": 139.7715, "region": "tokyo" },
  "Bills": { "lat": 35.6695, "lng": 139.7060, "region": "tokyo" },
  "Afuri": { "lat": 35.6716, "lng": 139.7030, "region": "tokyo" },
  "Uobei": { "lat": 35.6595, "lng": 139.6985, "region": "tokyo" },
  "Hoto": { "lat": 35.5042, "lng": 138.7588, "region": "tokyo" },
  "Coco": { "lat": 35.6805, "lng": 139.7690, "region": "tokyo" },
  "Ekiben": { "lat": 35.6812, "lng": 139.7671, "region": "tokyo" },
  "Konbini": { "lat": 35.6329, "lng": 139.8804, "region": "tokyo" }, # Near Disney
  "Curry": { "lat": 35.6329, "lng": 139.8804, "region": "tokyo" }, # Hungry Bear
  "Queen of Hearts": { "lat": 35.6329, "lng": 139.8804, "region": "tokyo" },
  "Gyukatsu": { "lat": 35.6984, "lng": 139.7708, "region": "tokyo" },

  "Kinryu": { "lat": 34.6687, "lng": 135.5038, "region": "osaka" },
  "Kani": { "lat": 34.6688, "lng": 135.5013, "region": "osaka" },
  "Mizuno": { "lat": 34.6684, "lng": 135.5030, "region": "osaka" },
  "Takoyaki": { "lat": 34.6690, "lng": 135.5035, "region": "osaka" },
  "Butterbeer": { "lat": 34.6654, "lng": 135.4323, "region": "osaka" },
  "Mario": { "lat": 34.6658, "lng": 135.4300, "region": "osaka" },
  "551": { "lat": 34.6655, "lng": 135.5015, "region": "osaka" },
  "Takeru": { "lat": 34.6625, "lng": 135.5060, "region": "osaka" },
  "Daruma": { "lat": 34.6515, "lng": 135.5065, "region": "osaka" },
  "Tamade": { "lat": 34.6665, "lng": 135.5080, "region": "osaka" },
  "Kura": { "lat": 34.8055, "lng": 135.5315, "region": "osaka" },
  "Rikimaru": { "lat": 34.6650, "lng": 135.5010, "region": "osaka" },
  "Rikuro": { "lat": 34.6652, "lng": 135.5012, "region": "osaka" },
  "Endo": { "lat": 34.6875, "lng": 135.4845, "region": "osaka" },
  "Airport": { "lat": 34.4345, "lng": 135.2345, "region": "osaka" }
}

file_path = r"c:\Python\code\東京\Japan_Trip_Plan_Final_v10.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update the JavaScript Data Arrays
# We need to inject these new locations into tokyoLocations and osakaLocations
# Find the arrays in the script
tokyo_loc_pattern = r'(var tokyoLocations = \[)(.*?)(\];)'
osaka_loc_pattern = r'(var osakaLocations = \[)(.*?)(\];)'

# Helper to format JS object
def format_loc(name, lat, lng):
    return f'{{ name: "{name}", lat: {lat}, lng: {lng} }}'

# Prepare new entries
new_tokyo_entries = []
new_osaka_entries = []

for key, data in food_locations.items():
    # We use the key as a partial match for the name later, but for the map marker we want a nice name
    # We can try to extract the full name from the HTML if we wanted, but for now let's use the key or a mapped name
    # Actually, the key is from my map, let's just use the key as the name for the marker for simplicity, 
    # or better, we don't strictly need to add them to the initial array if we just want the button to work.
    # BUT, for the button to work with `focusMap`, the marker needs to exist on the map?
    # The current `focusMap` implementation:
    # map.eachLayer(function (layer) { if (layer.getLatLng && ... ) layer.openPopup(); });
    # So yes, the marker MUST be on the map.
    
    entry = format_loc(key + " (Food)", data['lat'], data['lng'])
    if data['region'] == 'tokyo':
        new_tokyo_entries.append(entry)
    else:
        new_osaka_entries.append(entry)

# Inject into Tokyo Array
def update_tokyo_array(match):
    existing = match.group(2)
    # Check if already exists to avoid duplicates (simple check)
    additions = []
    for entry in new_tokyo_entries:
        if entry.split(',')[1] not in existing: # Check lat to avoid dupes roughly
            additions.append(entry)
    
    if additions:
        return match.group(1) + existing + ",\n        " + ",\n        ".join(additions) + match.group(3)
    return match.group(0)

content = re.sub(tokyo_loc_pattern, update_tokyo_array, content, flags=re.DOTALL)

# Inject into Osaka Array
def update_osaka_array(match):
    existing = match.group(2)
    additions = []
    for entry in new_osaka_entries:
        if entry.split(',')[1] not in existing:
            additions.append(entry)
            
    if additions:
        return match.group(1) + existing + ",\n        " + ",\n        ".join(additions) + match.group(3)
    return match.group(0)

content = re.sub(osaka_loc_pattern, update_osaka_array, content, flags=re.DOTALL)


# 2. Update the Buttons to call focusMap
# Pattern: <a href="https://www.google.com/maps/search/?api=1&query=..." target="_blank" class="food-map-link">📍</a>
# We need to match the previous food item to know which key to use.
# This is tricky because the key in `food_locations` (e.g. "Mutekiya") matches the `alt` tag in the image!
# <img src="..." alt="Mutekiya">
# So we can look for the alt tag in the preceding lines.

# Strategy: Iterate through the file, find the food block, extract alt, look up coords, replace button.

# Regex to find the whole block:
# <a href="..." class="food-item"> ... <img ... alt="KEY"> ... </a> \s* <a href="..." class="food-map-link">📍</a>
pattern = re.compile(r'(<a href="[^"]+" target="_blank" class="food-item">.*?<img\s+src="[^"]+"\s+alt="([^"]+)">.*?</a>\s*)<a href="[^"]+" target="_blank" class="food-map-link">📍</a>', re.DOTALL)

def replace_button(match):
    full_block = match.group(1)
    alt_key = match.group(2)
    
    if alt_key in food_locations:
        data = food_locations[alt_key]
        lat = data['lat']
        lng = data['lng']
        region = data['region']
        
        # New button calling JS
        # href="javascript:void(0)" onclick="focusMap(lat, lng, 'region')"
        new_button = f'<a href="javascript:void(0)" onclick="focusMap({lat}, {lng}, \'{region}\')" class="food-map-link">📍</a>'
        return full_block + new_button
    else:
        # If key not found (e.g. some I missed), keep original or print warning
        print(f"Warning: No coordinates found for {alt_key}")
        return match.group(0) # No change

new_content, count = pattern.subn(replace_button, content)
print(f"Updated {count} buttons to use interactive map.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
