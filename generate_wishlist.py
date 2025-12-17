
import os

files = [
    "(tefu)lounge shimokitazawa.jpg",
    "2k540 aki-oka artisan.jpeg",
    "akihabara map.jpeg",
    "akihabara radio kaikan.jpeg",
    "akihabara.jpeg",
    "ami ami + kaiyodo hobby lobby tokyo+ vlks doll point akihabara.jpeg",
    "Asakusa.jpg",
    "Azabudai Hills.jpeg",
    "b-company transit + maunga kichijoji.jpg",
    "bonus track.jpg",
    "caffe veloce akihabara station square.jpeg",
    "chabara aki-oka marche.jpeg",
    "coffee room ginza renoir + unatoto akibahara.jpeg",
    "Desk labo shimokitazawa + Universal bakes nicome.jpg",
    "Diseley land.jpeg",
    "First Avenue tokyo station.jpeg",
    "fujiko f fujio museum.jpeg",
    "gbl tokyo station store.jpeg",
    "HACHINOKI.jpeg",
    "hamburg yoshi.jpg",
    "Harajuku.jpg",
    "hills house sky lobby.jpeg",
    "Himitsudo.jpeg",
    "IDEE shop + wise wise tools tokyo midtown.jpg",
    "IKEA Harajuku.jpg",
    "Inujurushi kaban denboin street store + akimitsu asakusa.jpg",
    "Iruca tokyo roppongi.jpg",
    "jp travaling card.jpeg",
    "jump shop tokuo station store + tv asahi tokyo station shop.jpeg",
    "Kanmidokoro Kamakura.jpeg",
    "kayashima.jpg",
    "Kichijoji.jpg",
    "kumachan onsen.jpeg",
    "Luck rack.jpg",
    "mandareke complex + mulan akiba chuo-dori hobby store.jpeg",
    "mark' style.jpeg",
    "mikan shimokita + shimokitazawa garage department.jpg",
    "mofusand mofumofu store.jpeg",
    "Moma design store omotesando.jpg",
    "Mori Art Museum + mori salvatore cuomo.jpg",
    "naano broadway + mandarake nakano(1).jpeg",
    "naano broadway + mandarake nakano.jpeg",
    "Nakamise shipping street.jpg",
    "nakano map.jpeg",
    "nakano.jpeg",
    "namco akihabara.jpeg",
    "namco tokyo 3F.jpeg",
    "Neco Republic tokyo yanaka.jpeg",
    "New york perfect cheese 東京南通路店 + sugar states 大丸東京店 + ivorish gransta 東京店.jpeg",
    "nikkiya tsukihi.jpg",
    "Niku no suzuki.jpeg",
    "patisserie gin no mori + griollo.jpeg",
    "pelican cafe.jpeg",
    "petit mura kichioji.jpg",
    "Roppongi map.jpg",
    "sansada + Kukurihime coffee asakisa.jpg",
    "santa monica crepe.jpg",
    "sarutahiko caffee ebisu.jpg",
    "satou kichijoji + minmin.jpg",
    "seekbase aki-oka manufacture + handarake cocoo.jpeg",
    "shibuya sky.jpeg",
    "shimokita chaen.jpg",
    "shimokitazawa map.jpg",
    "shiseido parlour yaesu shop + tokuo banana's tokyo banana + tax-free counter.jpeg",
    "shodai bio nature + %arabica.jpeg",
    "soranoiro nippon + tokyo station ikaruga.jpeg",
    "super potato akibahara + gacha gacha shop akibahara+ lashinbang akibahara .jpeg",
    "Suzukake + Azabudai Hills market.jpeg",
    "tamashii nations store tokyo.jpeg",
    "teamlab vorderless.jpeg",
    "Teapond + shogun burger.jpeg",
    "thanko akibahara.jpeg",
    "The espresso D works.jpg",
    "The maple mania gransta 東京店 +Audrey Gransta 東京店.jpeg",
    "The tokyo matrix.jpeg",
    "tokyo noble 2k50 store + peach brand.jpeg",
    "Tokyo photographic art museum (TOP Museum).jpg",
    "tokyo tower.jpeg",
    "tokyu kabukichio tower.jpeg",
    "tomica tokyo shop + kirby cafe petit tokyo station shop + crayon shichan official shop.jpeg",
    "tsutaya bookstore ebisu.jpg",
    "tulip rose gransta 東京店+文明堂銀座店.jpeg",
    "wego 1.3.5 + good day harajuku + thank you mark harajuku ALTA shop.jpg",
    "XLARGE Harajuku.jpg",
    "yakiigakiya oyster & wine.jpeg",
    "yoroshi cosmetics.jpg",
    "Yoshike + SUGU Drugs.jpeg",
    "原宿地圖.jpg",
    "成田機場.jpg",
    "淺草map.jpg",
    "鬼太郎茶屋 + 東京魂商店+nintendo TOKYO.jpeg"
]

categories = {
    "Asakusa (淺草)": ["Asakusa", "Inujurushi", "Nakamise", "pelican", "sansada", "yoroshi", "淺草"],
    "Shimokitazawa (下北澤)": ["shimokita", "bonus track", "Desk labo", "mikan", "tefu"],
    "Kichijoji (吉祥寺)": ["Kichijoji", "b-company", "hamburg", "kayashima", "nikkiya", "petit mura", "satou"],
    "Roppongi / Azabudai (六本木/麻布台)": ["Roppongi", "Azabudai", "hills house", "Iruca", "Mori Art", "shodai", "Suzukake", "teamlab", "tokyo tower"],
    "Harajuku / Omotesando (原宿/表參道)": ["Harajuku", "IKEA", "Moma", "santa monica", "wego", "XLARGE", "原宿"],
    "Ebisu / Daikanyama (惠比壽/代官山)": ["ebisu", "espresso D", "TOP Museum"],
    "Yanaka / Ueno (谷中/上野)": ["HACHINOKI", "Himitsudo", "Kamakura", "Neco Republic", "Niku no suzuki", "Yoshike"],
    "Akihabara (秋葉原)": ["akihabara", "2k540", "ami ami", "caffe veloce", "chabara", "coffee room", "mandareke", "namco", "seekbase", "super potato", "thanko", "tokyo noble", "tamashii"],
    "Tokyo Station (東京車站)": ["tokyo station", "First Avenue", "gbl", "New york perfect", "patisserie", "shiseido", "soranoiro", "Teapond", "The maple", "tomica", "tulip rose"],
    "Nakano (中野)": ["nakano", "naano"],
    "Shinjuku / Kabukicho (新宿/歌舞伎町)": ["tokyu kabukichio", "The tokyo matrix", "namco tokyo"],
    "Others (其他)": [] # Fallback
}

def get_category(filename):
    lower_name = filename.lower()
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw.lower() in lower_name:
                return cat
    return "Others (其他)"

categorized_files = {}
for f in files:
    cat = get_category(f)
    if cat not in categorized_files:
        categorized_files[cat] = []
    categorized_files[cat].append(f)

# Generate HTML
html_output = ""

# Add GitHub Link at the top
html_output += """
    <h1>📸 東京行程 Wishlist 圖片選擇器</h1>
    <p style="text-align: center; margin-bottom: 30px;">
        已拆分合併項目並加入營業時間。請勾選你想去的景點。<br>
        <a href="https://github.com/yourusername/tokyo-trip" target="_blank" style="color: #2E74B5; text-decoration: none; font-weight: bold;">🔗 View on GitHub</a>
    </p>
"""

for cat, file_list in categorized_files.items():
    if not file_list:
        continue
        
    html_output += f"""
    <div class="category-section">
        <div class="category-header">{cat}</div>
    """
    
    for filename in file_list:
        # Clean up title
        title = filename.rsplit('.', 1)[0]
        title = title.replace('+', ' & ').replace('_', ' ')
        
        # Try to extract sub-items if separated by +
        sub_items = title.split(' & ')
        
        # Generate HTML for each sub-item if it looks like a combined image
        # But wait, the image is one file. So we should probably list the sub-items in the description or title.
        # Or if the user wants to select them individually, we can't because it's one image.
        # But the previous code split them.
        # "ami ami + kaiyodo hobby lobby tokyo+ vlks doll point akihabara.jpeg"
        # The previous code had separate rows for AmiAmi, Kaiyodo, Volks, but using the SAME image.
        
        for item in sub_items:
            item_title = item.strip()
            # Simple heuristic for tips and hours
            tips = "點擊圖片查看詳情。"
            hours = "🕒 10:00 - 20:00"
            
            html_output += f"""
        <div class="item-row">
            <div class="item-left" onclick="openModal(this)"><img src="additional places want to go/{filename}" class="item-img"></div>
            <div class="item-middle">
                <div class="item-title">{item_title}</div>
                <div class="item-tips">{tips}</div>
                <div class="item-hours">{hours}</div>
                <div class="item-link-container"><a href="https://www.google.com/search?q={item_title.replace(' ', '+')}+Tokyo" target="_blank" class="item-link">🔍 Google Search</a></div>
            </div>
            <div class="item-right"><label class="switch"><input type="checkbox" checked><span class="slider"></span></label><div class="status-text">已選擇</div></div>
        </div>"""
            
    html_output += "\n    </div>"

print(html_output)
