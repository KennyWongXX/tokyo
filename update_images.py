import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

v8_content = read_file(r'c:\Python\code\東京\Japan_Trip_Plan_Final_v8.html')

# Mapping of placeholder text keywords to new Image URLs
image_map = {
    "Mutekiya+Ramen": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Mutekiya_Ramen_at_INDIGO_Beijing_%2820220926155707%29.jpg/640px-Mutekiya_Ramen_at_INDIGO_Beijing_%2820220926155707%29.jpg",
    "Torikizoku": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Yakitori_001.jpg/640px-Yakitori_001.jpg",
    "Konbini+Food": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Onigiri_wrapped_in_nori_2.jpg/640px-Onigiri_wrapped_in_nori_2.jpg",
    "Curry+Rice": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Katsu_Curry_Rice.jpg/640px-Katsu_Curry_Rice.jpg",
    "Alice+Restaurant": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Strawberry_Parfait_at_Fruits_Parlor_Takano.jpg/640px-Strawberry_Parfait_at_Fruits_Parlor_Takano.jpg",
    "Maid+Cafe": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Omu-rice_by_f_a_r_e_w_e_l_l_in_Akihabara%2C_Tokyo.jpg/640px-Omu-rice_by_f_a_r_e_w_e_l_l_in_Akihabara%2C_Tokyo.jpg",
    "Gyukatsu": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Beef_katsu_set_meal.jpg/640px-Beef_katsu_set_meal.jpg",
    "Cheese+Tart": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Cheese_tart.jpg/640px-Cheese_tart.jpg",
    "Bills+Pancakes": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Ricotta_hotcakes_bills_Omotesando.jpg/640px-Ricotta_hotcakes_bills_Omotesando.jpg",
    "Afuri+Ramen": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Yuzu_Shio_Ramen_%40_Afuri_%40_Ebisu_%2814018023979%29.jpg/640px-Yuzu_Shio_Ramen_%40_Afuri_%40_Ebisu_%2814018023979%29.jpg",
    "Uobei+Sushi": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Conveyor_belt_sushi_by_jpellgen.jpg/640px-Conveyor_belt_sushi_by_jpellgen.jpg",
    "Hoto+Noodles": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Hoto_noodle.jpg/640px-Hoto_noodle.jpg",
    "Coco+Curry": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Curry_rice_by_shibainu.jpg/640px-Curry_rice_by_shibainu.jpg",
    "Chinese+Food": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Mapo_doufu_by_su-lin.jpg/640px-Mapo_doufu_by_su-lin.jpg",
    "Pizza+Pasta": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/640px-Eq_it-na_pizza-margherita_sep2005_sml.jpg",
    "Ekiben": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Ekiben_Daruma_Bento.jpg/640px-Ekiben_Daruma_Bento.jpg",
    "Kinryu+Ramen": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Kinryu-Noodle1.jpg/640px-Kinryu-Noodle1.jpg",
    "Crab+Lunch": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Kani_Doraku_Dotombori_Higashi_mise.jpg/640px-Kani_Doraku_Dotombori_Higashi_mise.jpg",
    "Okonomiyaki": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Okonomiyaki_001.jpg/640px-Okonomiyaki_001.jpg",
    "Takoyaki": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Takoyaki_by_D.jpg/640px-Takoyaki_by_D.jpg",
    "Butterbeer": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Butterbeer_at_Universal_Studios_Hollywood.jpg/640px-Butterbeer_at_Universal_Studios_Hollywood.jpg",
    "Mario+Burger": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cheeseburger.jpg/640px-Cheeseburger.jpg",
    "Pork+Bun": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Nikuman_steamed_pork_bun.jpg/640px-Nikuman_steamed_pork_bun.jpg",
    "Steak+Bowl": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Steak_don.jpg/640px-Steak_don.jpg",
    "Kushikatsu": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Kushikatsu_Daruma.jpg/640px-Kushikatsu_Daruma.jpg",
    "Supermarket": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Super_Tamade_Ohike.jpg/640px-Super_Tamade_Ohike.jpg",
    "Kura+Sushi": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Kura_Sushi_Shinsekai-Tsutenkaku.jpg/640px-Kura_Sushi_Shinsekai-Tsutenkaku.jpg",
    "Yakiniku+BBQ": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Yakiniku_001.jpg/640px-Yakiniku_001.jpg",
    "Cheesecake": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Cheesecake_slice.jpg/640px-Cheesecake_slice.jpg",
    "Endo+Sushi": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Nigiri_sushi_set.jpg/640px-Nigiri_sushi_set.jpg",
    "Airport+Food": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Kitsune_Udon_001.jpg/640px-Kitsune_Udon_001.jpg"
}

# Replace placeholder URLs
# Pattern: src="https://placehold.co/300x200/.*?text=(.*?)"
def replace_image(match):
    text_key = match.group(1)
    # Remove color codes if present in regex match (though my regex above captures text after ?text=)
    # The actual URL is like: https://placehold.co/300x200/d35400/fff?text=Mutekiya+Ramen
    # So we need to be careful.
    
    # Let's just search for the key in the map
    for key, url in image_map.items():
        if key == text_key:
            return f'src="{url}"'
    
    return match.group(0) # No change if not found

# We need a regex that captures the whole src attribute
# src="https://placehold.co/300x200/[a-f0-9]+/[a-f0-9]+\?text=([a-zA-Z0-9+]+)"
new_content = re.sub(r'src="https://placehold.co/300x200/[a-f0-9]+/[a-f0-9]+\?text=([a-zA-Z0-9+]+)"', replace_image, v8_content)

with open(r'c:\Python\code\東京\Japan_Trip_Plan_Final_v8.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Images updated successfully")
