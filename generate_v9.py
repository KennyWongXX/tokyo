
import os

# Define the source and destination files
source_file = 'Japan_Trip_Plan_Final_v7.html'
output_file = 'Japan_Trip_Plan_Final_v9.html'

# Read the content of the source file
with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the JavaScript to include the focusMap function and updated locations
# We will replace the existing script block with a new one
old_script_start = "var tokyoLocations = ["
new_script_logic = """
    function focusMap(lat, lng, mapId) {
        var map = mapId === 'tokyo' ? mapTokyo : mapOsaka;
        map.setView([lat, lng], 16);
        var mapElement = document.getElementById('map-' + mapId);
        mapElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Open popup
        map.eachLayer(function (layer) {
            if (layer.getLatLng && Math.abs(layer.getLatLng().lat - lat) < 0.0001 && Math.abs(layer.getLatLng().lng - lng) < 0.0001) {
                layer.openPopup();
            }
        });
    }

    var tokyoLocations = [
        { name: "成田機場 (NRT)", lat: 35.7719, lng: 140.3907 },
        { name: "池袋 (住宿/玩樂)", lat: 35.7295, lng: 139.7109 },
        { name: "無敵家拉麵", lat: 35.7278, lng: 139.7115 },
        { name: "GIGO 池袋總店", lat: 35.729603, lng: 139.7148759 },
        { name: "Round 1 池袋", lat: 35.7290751, lng: 139.7209701 },
        { name: "Tokyo Disneyland", lat: 35.6329, lng: 139.8804 },
        { name: "Tokyo DisneySea", lat: 35.6267, lng: 139.8851 },
        { name: "秋葉原 (動漫)", lat: 35.6984, lng: 139.7731 },
        { name: "Radio Kaikan (秋葉原)", lat: 35.6979966, lng: 139.7719706 },
        { name: "牛かつもと村 (秋葉原)", lat: 35.6984060, lng: 139.7708850 },
        { name: "@Home Cafe (秋葉原)", lat: 35.6995541, lng: 139.7707877 },
        { name: "淺草寺 (Sensoji)", lat: 35.7134032, lng: 139.7955265 },
        { name: "澀谷 (Sky/Parco)", lat: 35.6580, lng: 139.7016 },
        { name: "Shibuya Sky", lat: 35.6582857, lng: 139.7022617 },
        { name: "Shibuya Parco", lat: 35.6618780, lng: 139.6987379 },
        { name: "挽肉と米 (澀谷)", lat: 35.6593756, lng: 139.6987796 },
        { name: "原宿 (竹下通)", lat: 35.6702, lng: 139.7027 },
        { name: "富士急樂園", lat: 35.4869, lng: 138.7806 }
    ];

    tokyoLocations.forEach(function(loc) {
        L.marker([loc.lat, loc.lng]).addTo(mapTokyo)
            .bindPopup("<b>" + loc.name + "</b>");
    });

    // Initialize Osaka Map
    var mapOsaka = L.map('map-osaka').setView([34.6937, 135.5023], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mapOsaka);

    var osakaLocations = [
        { name: "難波/道頓堀 (住宿/Glico)", lat: 34.6687, lng: 135.5013 },
        { name: "黑門市場", lat: 34.6653277, lng: 135.5069795 },
        { name: "美津の大阪燒", lat: 34.6684527, lng: 135.5030691 },
        { name: "USJ 環球影城", lat: 34.6654, lng: 135.4323 },
        { name: "日本橋 (動漫)", lat: 34.6595, lng: 135.5060 },
        { name: "Super Kids Land (日本橋)", lat: 34.6592857, lng: 135.5056097 },
        { name: "通天閣 (新世界)", lat: 34.6525, lng: 135.5063 },
        { name: "元祖串炸 Daruma (新世界)", lat: 34.6688482, lng: 135.5030746 },
        { name: "Jumbo 釣船茶屋", lat: 34.6520901, lng: 135.5061908 },
        { name: "Expocity (萬博)", lat: 34.8056, lng: 135.5322 },
        { name: "奈良公園", lat: 34.6850, lng: 135.8430 },
        { name: "關西機場 (KIX)", lat: 34.4320, lng: 135.2304 }
    ];

    osakaLocations.forEach(function(loc) {
        L.marker([loc.lat, loc.lng]).addTo(mapOsaka)
            .bindPopup("<b>" + loc.name + "</b>");
    });
"""

# Find where the old script starts and replace the rest of the script block
# We'll look for "var tokyoLocations = [" and replace until the end of the script tag
if old_script_start in content:
    parts = content.split(old_script_start)
    # Keep the part before
    pre_script = parts[0]
    # The part after contains the rest of the script and the closing tags
    # We need to find where the script ends to preserve </body></html>
    # But since the script is at the end, we can just replace the script block.
    # However, let's be safer. We will replace the specific block we know.
    
    # Actually, simpler approach: Replace the specific variable definitions and add the function
    # But since we want to replace the whole logic, let's find the range.
    
    # Let's just replace the known block of code for tokyoLocations and osakaLocations
    # and insert the function before it.
    pass

# 2. Replace HTML Links with OnClick events
# Define replacements (Old String -> New String)
replacements = [
    # Tokyo Replacements
    (
        '<a href="https://www.google.com/maps/search/GIGO+Ikebukuro" target="_blank" class="map-link">📍GIGO 地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.729603, 139.7148759, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Round+1+Ikebukuro" target="_blank" class="map-link">📍Round 1 地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.7290751, 139.7209701, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Mutekiya+Ramen" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.7278, 139.7115, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Tokyo+Disneyland" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.6329, 139.8804, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Tokyo+DisneySea" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.6267, 139.8851, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Sensoji+Temple" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.7134032, 139.7955265, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Akihabara+Station" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.6984, 139.7731, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Gyukatsu+Motomura+Akihabara" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.6984060, 139.7708850, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/At+Home+Cafe+Akihabara" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.6995541, 139.7707877, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Harajuku+Station" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.6702, 139.7027, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Shibuya+Station" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.6580, 139.7016, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Hikiniku+to+Come+Shibuya" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.6593756, 139.6987796, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Fuji-Q+Highland" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(35.4869, 138.7806, \'tokyo\')" class="map-link">📍在地圖查看</a>'
    ),
    # Osaka Replacements
    (
        '<a href="https://www.google.com/maps/search/Kuromon+Market" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(34.6653277, 135.5069795, \'osaka\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Dotonbori+Glico+Man" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(34.6687, 135.5013, \'osaka\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Mizuno+Okonomiyaki" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(34.6684527, 135.5030691, \'osaka\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Universal+Studios+Japan" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(34.6654, 135.4323, \'osaka\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Den+Den+Town" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(34.6595, 135.5060, \'osaka\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Tsutenkaku" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(34.6525, 135.5063, \'osaka\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Kushikatsu+Daruma+Shinsekai" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(34.6688482, 135.5030746, \'osaka\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Jumbo+Fishing+Restaurant+Osaka" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(34.6520901, 135.5061908, \'osaka\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Expocity+Osaka" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(34.8056, 135.5322, \'osaka\')" class="map-link">📍在地圖查看</a>'
    ),
    (
        '<a href="https://www.google.com/maps/search/Nara+Park" target="_blank" class="map-link">📍地圖</a>',
        '<a href="javascript:void(0)" onclick="focusMap(34.6850, 135.8430, \'osaka\')" class="map-link">📍在地圖查看</a>'
    )
]

# Perform replacements
for old, new in replacements:
    content = content.replace(old, new)

# Replace the script part
# We will identify the block starting from "var tokyoLocations = [" to the end of the script tag
# Since we know the structure, we can split by "var tokyoLocations = [" and then find the end of the script
if "var tokyoLocations = [" in content:
    pre_script = content.split("var tokyoLocations = [")[0]
    # Find the end of the script tag
    post_script_parts = content.split("</script>")
    # The last part is </body></html>, the second to last is the end of our script
    # This is a bit risky if there are multiple script tags, but here we only have one at the end.
    # Let's use a safer replace.
    
    # We will construct the new content by taking everything before "var tokyoLocations = ["
    # appending our new script logic, and then appending "</script>" and the rest.
    
    # Find the index of "var tokyoLocations = ["
    idx = content.find("var tokyoLocations = [")
    
    # Find the index of the closing script tag after that
    end_idx = content.find("</script>", idx)
    
    new_content = content[:idx] + new_script_logic + content[end_idx:]
    content = new_content

# Write the new file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully created {output_file}")
