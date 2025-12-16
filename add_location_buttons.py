import re

file_path = r"c:\Python\code\東京\Japan_Trip_Plan_Final_v10.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS
# Find the .food-item CSS and update margin, and add .food-map-link
css_pattern = r'(\.food-item\s*\{[^}]*margin-right:\s*)10px(;|})'
if re.search(css_pattern, content):
    content = re.sub(css_pattern, r'\1 2px\2', content)
    print("Updated .food-item margin.")
else:
    print("Could not find .food-item margin to update.")

# Add .food-map-link CSS
new_css = """
    .food-map-link {
        text-decoration: none;
        margin-left: 2px;
        margin-right: 10px;
        font-size: 1em;
        cursor: pointer;
    }
"""
# Insert before the closing </style>
content = content.replace("</style>", new_css + "</style>")


# 2. Add Location Buttons
# Regex to find food items
# We capture:
# 1. The opening tag and text before span
# 2. The text content (name)
# 3. The rest of the tag (span and closing a)
pattern = re.compile(r'(<a href="[^"]+" target="_blank" class="food-item">\s*)(.*?)\s*(<span class="food-popup">.*?</span>\s*</a>)', re.DOTALL)

def replace_food_item(match):
    full_match = match.group(0)
    name_raw = match.group(2)
    
    # Clean name for query: remove parentheses and time info
    # e.g. "無敵家拉麵 (10:30-04:00)" -> "無敵家拉麵"
    name_clean = re.sub(r'\s*\(.*?\)', '', name_raw).strip()
    
    # If name is empty (unlikely), fallback to raw
    if not name_clean:
        name_clean = name_raw.strip()
        
    # Construct Google Maps Search URL
    # Using query parameter
    map_url = f"https://www.google.com/maps/search/?api=1&query={name_clean}"
    
    # Append the map link
    return f'{full_match}\n            <a href="{map_url}" target="_blank" class="food-map-link">📍</a>'

# Apply replacement
new_content, count = pattern.subn(replace_food_item, content)

print(f"Added {count} location buttons.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
