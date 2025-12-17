import os
import urllib.parse

# Configuration
IMAGE_DIR = "additional places want to go"
OUTPUT_FILE = "Wishlist_Selection.html"

# Categories and Keywords
categories = {
    "Asakusa (淺草)": ["Asakusa", "Inujurushi", "Nakamise", "pelican", "sansada", "yoroshi", "淺草", "Kukurihime", "Akimitsu"],
    "Shimokitazawa (下北澤)": ["shimokita", "bonus track", "Desk labo", "mikan", "tefu", "Universal bakes", "Garage Department"],
    "Kichijoji (吉祥寺)": ["Kichijoji", "b-company", "hamburg", "kayashima", "nikkiya", "petit mura", "satou", "Minmin", "Maunga"],
    "Roppongi / Azabudai (六本木/麻布台)": ["Roppongi", "Azabudai", "hills house", "Iruca", "Mori Art", "shodai", "Suzukake", "teamlab", "tokyo tower", "Salvatore Cuomo", "Arabica"],
    "Harajuku / Omotesando (原宿/表參道)": ["Harajuku", "IKEA", "Moma", "santa monica", "wego", "XLARGE", "原宿", "good day", "thank you mark"],
    "Ebisu / Daikanyama (惠比壽/代官山)": ["ebisu", "espresso D", "TOP Museum", "tsutaya"],
    "Yanaka / Ueno (谷中/上野)": ["HACHINOKI", "Himitsudo", "Kamakura", "Neco Republic", "Niku no suzuki", "Yoshike", "Sugi Drug"],
    "Akihabara (秋葉原)": ["akihabara", "2k540", "ami ami", "caffe veloce", "chabara", "coffee room", "mandareke", "namco", "seekbase", "super potato", "thanko", "tokyo noble", "tamashii", "kaiyodo", "volks", "lashinbang", "gacha", "radio kaikan", "mulan", "unatoto", "ginza renoir"],
    "Tokyo Station (東京車站)": ["tokyo station", "First Avenue", "gbl", "New york perfect", "patisserie", "shiseido", "soranoiro", "Teapond", "The maple", "tomica", "tulip rose", "jump shop", "tv asahi", "mofusand", "audrey", "sugar butter", "ivorish", "ikaruga", "bunmeido", "mark's style", "kirby", "crayon"],
    "Nakano (中野)": ["nakano", "naano", "mandarake nakano"],
    "Shinjuku / Kabukicho (新宿/歌舞伎町)": ["tokyu kabukichio", "The tokyo matrix", "namco tokyo", "shogun burger"],
    "Others (其他)": [] # Fallback
}

def get_category(filename):
    lower_name = filename.lower()
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw.lower() in lower_name:
                return cat
    return "Others (其他)"

# HTML Templates
HTML_HEADER = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>東京行程 Wishlist 圖片選擇器 (Total: {total_count})</title>
<style>
    body {{ font-family: "Microsoft JhengHei", sans-serif; background-color: #f0f2f5; padding: 20px; color: #333; }}
    h1 {{ text-align: center; margin-bottom: 30px; }}
    .container {{ max-width: 1000px; margin: 0 auto; }}
    
    .category-section {{ background: white; border-radius: 10px; margin-bottom: 30px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
    .category-header {{ background-color: #2E74B5; color: white; padding: 15px 20px; font-size: 1.3em; font-weight: bold; }}
    
    .item-row {{ display: flex; align-items: center; border-bottom: 1px solid #eee; padding: 15px; transition: background-color 0.2s; }}
    .item-row:last-child {{ border-bottom: none; }}
    .item-row:hover {{ background-color: #f9f9f9; }}
    
    .item-left {{ width: 120px; height: 90px; flex-shrink: 0; margin-right: 20px; border-radius: 6px; overflow: hidden; background-color: #eee; cursor: pointer; }}
    .item-img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }}
    .item-left:hover .item-img {{ transform: scale(1.1); }}
    
    .item-middle {{ flex-grow: 1; padding-right: 20px; }}
    .item-title {{ font-size: 1.1em; font-weight: bold; margin-bottom: 5px; color: #333; }}
    .item-tips {{ font-size: 0.9em; color: #555; margin-bottom: 3px; display: flex; align-items: center; }}
    .item-tips::before {{ content: "💡"; margin-right: 5px; }}
    .item-hours {{ font-size: 0.9em; color: #e65100; margin-bottom: 5px; display: flex; align-items: center; font-weight: 500; }}
    .item-link-container {{ margin-top: 5px; }}
    .item-link {{ font-size: 0.85em; color: #2E74B5; text-decoration: none; border: 1px solid #2E74B5; padding: 2px 8px; border-radius: 4px; transition: all 0.2s; display: inline-block; }}
    .item-link:hover {{ background-color: #2E74B5; color: white; }}
    
    .item-right {{ width: 100px; flex-shrink: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    
    /* Toggle Switch */
    .switch {{ position: relative; display: inline-block; width: 50px; height: 26px; margin-bottom: 5px; }}
    .switch input {{ opacity: 0; width: 0; height: 0; }}
    .slider {{ position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #ccc; transition: .4s; border-radius: 34px; }}
    .slider:before {{ position: absolute; content: ""; height: 20px; width: 20px; left: 3px; bottom: 3px; background-color: white; transition: .4s; border-radius: 50%; }}
    input:checked + .slider {{ background-color: #2196F3; }}
    input:focus + .slider {{ box-shadow: 0 0 1px #2196F3; }}
    input:checked + .slider:before {{ transform: translateX(24px); }}
    
    .status-text {{ font-size: 0.8em; color: #666; }}
    input:checked ~ .status-text {{ color: #2196F3; font-weight: bold; }}

    .summary-box {{ position: fixed; bottom: 20px; right: 20px; background: #333; color: white; padding: 15px 25px; border-radius: 30px; box-shadow: 0 5px 20px rgba(0,0,0,0.3); z-index: 1000; font-weight: bold; }}
    
    /* Modal */
    .modal {{ display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.9); }}
    .modal-content {{ margin: auto; display: block; max-width: 90%; max-height: 90%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }}
    .close {{ position: absolute; top: 20px; right: 35px; color: #f1f1f1; font-size: 40px; font-weight: bold; cursor: pointer; }}
</style>
</head>
<body>

<div class="container">
    <h1>📸 東京行程 Wishlist 圖片選擇器</h1>
    <p style="text-align: center; margin-bottom: 30px;">
        已拆分合併項目並加入營業時間。請勾選你想去的景點。<br>
        <a href="https://github.com/KennyWongXX/tokyo/blob/master/Wishlist_Selection.html" target="_blank" style="color: #2E74B5; text-decoration: none; font-weight: bold; margin-top: 10px; display: inline-block;">🔗 View on GitHub</a>
    </p>
"""

HTML_FOOTER = """
</div>

<div class="summary-box">
    <div class="summary-text">已選擇: <span id="count">0</span> / <span id="total-count">0</span></div>
</div>

<div id="myModal" class="modal">
  <span class="close" onclick="closeModal()">&times;</span>
  <img class="modal-content" id="img01">
</div>

<script>
    // Update count
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const countSpan = document.getElementById('count');
    const totalCountSpan = document.getElementById('total-count');
    
    totalCountSpan.textContent = checkboxes.length;
    
    function updateCount() {
        const checkedCount = document.querySelectorAll('input[type="checkbox"]:checked').length;
        countSpan.textContent = checkedCount;
    }

    checkboxes.forEach(box => {
        box.addEventListener('change', function() {
            updateCount();
            // Update status text
            const statusText = this.parentElement.nextElementSibling;
            if(this.checked) {
                statusText.textContent = "已選擇";
                statusText.style.color = "#2196F3";
                statusText.style.fontWeight = "bold";
            } else {
                statusText.textContent = "未選擇";
                statusText.style.color = "#999";
                statusText.style.fontWeight = "normal";
            }
        });
    });
    
    // Initial count
    updateCount();

    // Modal
    const modal = document.getElementById("myModal");
    const modalImg = document.getElementById("img01");
    
    function openModal(element) {
        modal.style.display = "block";
        modalImg.src = element.querySelector('img').src;
    }
    
    function closeModal() {
        modal.style.display = "none";
    }
    
    // Close modal when clicking outside
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
</script>

</body>
</html>
"""

# Main Logic
def generate():
    # Get all files
    try:
        files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    except FileNotFoundError:
        print(f"Error: Directory '{IMAGE_DIR}' not found.")
        return

    categorized_items = {cat: [] for cat in categories}
    total_items = 0

    for filename in files:
        cat = get_category(filename)
        
        # Clean up title
        title_raw = os.path.splitext(filename)[0]
        
        # Split logic: Split by '+' or '&'
        # Also handle " + " with spaces
        sub_items = title_raw.replace('+', '&').split('&')
        
        for item in sub_items:
            item_title = item.strip().replace('_', ' ')
            if not item_title: continue
            
            # Heuristics for display
            display_title = item_title
            
            # Generate HTML for this item
            # Note: We use the SAME image for all sub-items derived from one file
            
            # URL encode filename for src
            encoded_image_dir = urllib.parse.quote(IMAGE_DIR)
            encoded_filename = urllib.parse.quote(filename)
            img_src = f"{encoded_image_dir}/{encoded_filename}"
            search_query = urllib.parse.quote(display_title + ' Tokyo')
            
            html_item = f"""
        <div class="item-row">
            <div class="item-left" onclick="openModal(this)"><img src="{img_src}" class="item-img"></div>
            <div class="item-middle">
                <div class="item-title">{display_title}</div>
                <div class="item-tips">點擊圖片放大。</div>
                <div class="item-hours">🕒 10:00 - 20:00</div>
                <div class="item-link-container"><a href="https://www.google.com/search?q={search_query}" target="_blank" class="item-link">🔍 Google Search</a></div>
            </div>
            <div class="item-right"><label class="switch"><input type="checkbox" checked><span class="slider"></span></label><div class="status-text">已選擇</div></div>
        </div>"""
            
            categorized_items[cat].append(html_item)
            total_items += 1

    # Build Output
    final_html = HTML_HEADER.format(total_count=total_items)
    
    # Order categories as defined in the dictionary
    for cat, items in categorized_items.items():
        if items:
            final_html += f"""
    <div class="category-section">
        <div class="category-header">{cat}</div>
        {{''.join(items)}}
    </div>"""
            
    final_html += HTML_FOOTER
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print(f"Successfully generated {OUTPUT_FILE} with {total_items} items from {len(files)} files.")

if __name__ == "__main__":
    generate()
