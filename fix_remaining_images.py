import re

# Mapping of alt text to new simple image URLs
image_map = {
    "Konbini": "https://commons.wikimedia.org/wiki/Special:FilePath/Japanese_rice_balls_(onigiri).jpg",
    "Curry": "https://commons.wikimedia.org/wiki/Special:FilePath/Japanese_curry_rice_1_2021-11-28.jpeg",
    "Alice": "https://commons.wikimedia.org/wiki/Special:FilePath/Roast_Chicken_with_Potato_Wedges.jpg"
}

file_path = r"c:\Python\code\東京\Japan_Trip_Plan_Final_v9.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

for alt_key, new_url in image_map.items():
    # Pattern looks for: <img src="[anything]" alt="alt_key">
    # We use non-greedy match .*? for the src content
    pattern = rf'(<img\s+src=")([^"]+)("\s+alt="{alt_key}">)'
    
    # Check if it exists
    if re.search(pattern, content):
        print(f"Updating image for: {alt_key}")
        # Replace with new url
        content = re.sub(pattern, rf'\1{new_url}\3', content)
    else:
        print(f"Could not find image tag for: {alt_key}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Remaining images updated.")
