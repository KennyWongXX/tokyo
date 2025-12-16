import re

# Mapping of alt text to new simple image URLs
image_map = {
    "Torikizoku": "https://commons.wikimedia.org/wiki/Special:FilePath/Yakitori_001.jpg",
    "Alice": "https://commons.wikimedia.org/wiki/Special:FilePath/Strawberry_Parfait.jpg",
    "Mutekiya": "https://commons.wikimedia.org/wiki/Special:FilePath/Muteki_Ramen.jpg",
    "Ichiran": "https://commons.wikimedia.org/wiki/Special:FilePath/Tonkotsu_ramen.jpg",
    "Vulcania": "https://commons.wikimedia.org/wiki/Special:FilePath/Mapo_Tofu.jpg",
    "Sebastian": "https://commons.wikimedia.org/wiki/Special:FilePath/Pizza_Margherita_stu_spivack.jpg",
    "Ekiben": "https://commons.wikimedia.org/wiki/Special:FilePath/Train_station_box_lunches_in_Japan_called_eki_ben.jpg",
    "Maid Cafe": "https://commons.wikimedia.org/wiki/Special:FilePath/Omurice.jpg",
    "Gyukatsu": "https://commons.wikimedia.org/wiki/Special:FilePath/Gyukatsu_(46075415774).jpg",
    "PABLO": "https://commons.wikimedia.org/wiki/Special:FilePath/Freshly_baked_cheese_tarts_at_Sendai_Station.jpg",
    "Bills": "https://commons.wikimedia.org/wiki/Special:FilePath/Pancakes_(9433083466).jpg",
    "Afuri": "https://commons.wikimedia.org/wiki/Special:FilePath/Ramen_noodles-04.jpg",
    "Uobei": "https://commons.wikimedia.org/wiki/Special:FilePath/Sushi_assortment.jpg",
    "Hoto": "https://commons.wikimedia.org/wiki/Special:FilePath/Hoto_udon.jpg",
    "Coco": "https://commons.wikimedia.org/wiki/Special:FilePath/Japanese_Katsu_Curry_01.jpg",
    "Kinryu": "https://commons.wikimedia.org/wiki/Special:FilePath/Kinryu-Noodle1.jpg",
    "Kani": "https://commons.wikimedia.org/wiki/Special:FilePath/Japanese_Kani-Dōraku_cuisine_1.JPG",
    "Mizuno": "https://commons.wikimedia.org/wiki/Special:FilePath/Okonomiyaki_002.jpg",
    "Takoyaki": "https://commons.wikimedia.org/wiki/Special:FilePath/Osaka_Takoyaki.jpg",
    "Butterbeer": "https://commons.wikimedia.org/wiki/Special:FilePath/ButterbeerUniversalStudios.JPG",
    "Mario": "https://commons.wikimedia.org/wiki/Special:FilePath/Japanese_Hamburger_Lunch_Set.jpg",
    "551": "https://commons.wikimedia.org/wiki/Special:FilePath/Nikuman.jpg",
    "Takeru": "https://commons.wikimedia.org/wiki/Special:FilePath/Gyudon.jpg",
    "Daruma": "https://commons.wikimedia.org/wiki/Special:FilePath/KushikatsuDaruma01.jpg",
    "Tamade": "https://commons.wikimedia.org/wiki/Special:FilePath/Super_Tamade_(1).JPG",
    "Kura": "https://commons.wikimedia.org/wiki/Special:FilePath/Sushi_conyeyor_chain_1.jpg",
    "Rikimaru": "https://commons.wikimedia.org/wiki/Special:FilePath/Yakiniku_001.jpg",
    "Rikuro": "https://commons.wikimedia.org/wiki/Special:FilePath/Cheesecake.jpg",
    "Endo": "https://commons.wikimedia.org/wiki/Special:FilePath/Sushi_assortment.jpg",
    "Airport": "https://commons.wikimedia.org/wiki/Special:FilePath/Udon_by_udono-2.jpg"
}

file_path = r"c:\Python\code\東京\Japan_Trip_Plan_Final_v9.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Regex to find img tags with specific alt text and replace src
# Pattern: <img src="..." alt="KEY">
# We capture the part before src, the src content (which we ignore), and the part after src up to alt="KEY"
# This is a bit tricky with regex. Better to find the whole tag.

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

print("All images updated.")
