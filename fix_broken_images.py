import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

path = r'c:\Python\code\東京\Japan_Trip_Plan_Final_v8.html'
content = read_file(path)

# Replacements
replacements = {
    # Mutekiya
    r'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Mutekiya_Ramen_at_INDIGO_Beijing_%2820220926155707%29.jpg/640px-Mutekiya_Ramen_at_INDIGO_Beijing_%2820220926155707%29.jpg': 
    'https://upload.wikimedia.org/wikipedia/commons/2/28/Tonkotsu_ramen_in_Tokyo.jpg',
    
    # Afuri
    r'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Yuzu_Shio_Ramen_%40_Afuri_%40_Ebisu_%2814018023979%29.jpg/640px-Yuzu_Shio_Ramen_%40_Afuri_%40_Ebisu_%2814018023979%29.jpg': 
    'https://upload.wikimedia.org/wikipedia/commons/6/68/Shio_Ramen_001.jpg',
    
    # Omu-rice
    r'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Omu-rice_by_f_a_r_e_w_e_l_l_in_Akihabara%2C_Tokyo.jpg/640px-Omu-rice_by_f_a_r_e_w_e_l_l_in_Akihabara%2C_Tokyo.jpg': 
    'https://upload.wikimedia.org/wikipedia/commons/2/23/Omurice.jpg'
}

new_content = content
for old, new in replacements.items():
    new_content = new_content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed broken images.")
