import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

v5_content = read_file(r'c:\Python\code\東京\Japan_Trip_Plan_Final_v5.html')
v7_content = read_file(r'c:\Python\code\東京\Japan_Trip_Plan_Final_v7.html')

# 1. Extract Food CSS from v5
css_pattern = r'/\* Food Popup Styles \*/.*?(?=</style>)'
css_match = re.search(css_pattern, v5_content, re.DOTALL)
food_css = css_match.group(0) if css_match else ""

# 2. Extract Food Rows from v5
# We need to map v5 days to content.
# Strategy: Split v5 by "<h3>Day" to get chunks, then find food-row in each chunk.
v5_days = {}
parts = re.split(r'<h3>Day (\d+):', v5_content)
# parts[0] is header. parts[1] is day num, parts[2] is content, parts[3] is day num...
for i in range(1, len(parts), 2):
    day_num = int(parts[i])
    content = parts[i+1]
    food_row_match = re.search(r'<tr class="food-row">.*?</tr>', content, re.DOTALL)
    if food_row_match:
        v5_days[day_num] = food_row_match.group(0)

# 3. Extract Night Bus Section from v5
night_bus_pattern = r'<h2>🚌 關於夜間巴士 \(Night Bus\) 與行李</h2>.*?</ul>'
night_bus_match = re.search(night_bus_pattern, v5_content, re.DOTALL)
night_bus_section = night_bus_match.group(0) if night_bus_match else ""

# 4. Process v7
v8_content = v7_content

# Insert CSS
v8_content = v8_content.replace('</style>', f'\n{food_css}\n</style>')

# Remove existing .food-tag styles in v7 if we want to clean up, but keeping them is harmless.
# But we should probably remove the .food-row style in v7 if it conflicts or just let the new CSS override (it's later in file so it might, but v7 has it in <style> too).
# v7 has: .food-row { background-color: #fff0f5; color: #444; }
# v5 has: .food-row { background-color: #fff8e1; }
# I'll replace the v7 food-row style with v5's.
v8_content = v8_content.replace('.food-row { background-color: #fff0f5; color: #444; }', '')

# Mapping v7 Day -> v5 Day
day_mapping = {
    1: 1,
    2: 2,
    3: 6, # v7 Day 3 (DisneySea) <- v5 Day 6 (DisneySea)
    4: 3, # v7 Day 4 (Akiba) <- v5 Day 3 (Akiba)
    5: 4, # v7 Day 5 (Shibuya) <- v5 Day 4 (Shibuya)
    6: 5, # v7 Day 6 (FujiQ) <- v5 Day 5 (FujiQ)
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11
}

# Replace/Add Food Rows in v8
# We split v8 similarly
v8_parts = re.split(r'(<h3>Day \d+:)', v8_content)
# v8_parts[0] is header. v8_parts[1] is "<h3>Day 1:", v8_parts[2] is content...

new_v8_content = v8_parts[0]

for i in range(1, len(v8_parts), 2):
    header = v8_parts[i]
    content = v8_parts[i+1]
    
    # Extract day number from header
    day_num_match = re.search(r'Day (\d+):', header)
    if day_num_match:
        day_num = int(day_num_match.group(1))
        
        # Get the food row from v5
        source_day = day_mapping.get(day_num)
        food_row = v5_days.get(source_day, "")
        
        if day_num == 3: # Special handling for Day 3 (DisneySea) to remove "Ekiben" if present
             food_row = food_row.replace('<span class="food-category">[宵]</span>', '<!-- [宵] removed -->')
             # Regex to remove the link following it would be better, but let's see.
             # Actually, v5 Day 6 has Ekiben. v7 Day 3 is just DisneySea.
             # Let's just use it as is, or maybe replace the Ekiben part with something else or remove it.
             # Simple hack: remove the whole [宵] part for Day 3.
             food_row = re.sub(r'<span class="food-category">\[宵\].*?</a>', '', food_row, flags=re.DOTALL)

        if day_num == 6: # Special handling for Day 6 (FujiQ + Night Bus)
             # v5 Day 5 is FujiQ (Hoto, Coco).
             # v7 Day 6 is FujiQ + Night Bus.
             # We might want to ADD the Ekiben from v5 Day 6 here.
             ekiben_row = v5_days.get(6, "")
             ekiben_match = re.search(r'(<span class="food-category">\[宵\].*?</a>)', ekiben_row, re.DOTALL)
             if ekiben_match:
                 ekiben_html = ekiben_match.group(1)
                 # Append to food_row of Day 6 (which comes from v5 Day 5)
                 # v5 Day 5 ends with </td></tr>. We need to insert before </td>.
                 food_row = food_row.replace('</td>', f'\n            {ekiben_html}\n        </td>')

        # Remove existing food row in v7 content if any
        content = re.sub(r'<tr class="food-row">.*?</tr>', '', content, flags=re.DOTALL)
        
        # Insert new food row before </table>
        content = content.replace('</table>', f'{food_row}\n</table>')
    
    new_v8_content += header + content

# 5. Add Night Bus Section
# Insert before <script> (which is near the end in v7)
if '<script>' in new_v8_content:
    new_v8_content = new_v8_content.replace('<script>', f'{night_bus_section}\n\n<script>')
else:
    new_v8_content = new_v8_content.replace('</body>', f'{night_bus_section}\n</body>')

# Write v8
with open(r'c:\Python\code\東京\Japan_Trip_Plan_Final_v8.html', 'w', encoding='utf-8') as f:
    f.write(new_v8_content)

print("v8 created successfully")
