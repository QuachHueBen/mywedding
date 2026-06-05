import os
import re

base_dir = r"e:\AI_AGent\web-wedding"
index_file = os.path.join(base_dir, "index.html")

with open(index_file, "r", encoding="utf-8") as f:
    content = f.read()

for sec_id in ["album-studio", "album-nhatrai", "album-nhagai"]:
    btn = f'\n            <div class="view-all-container">\n                <button class="btn-view-all" onclick="toggleViewAll(this, \'{sec_id}\')">Xem chi tiết</button>\n            </div>\n        '
    
    pattern = rf'(<section id="{sec_id}".*?<div class="masonry-grid">.*?</div>)(\s*</div>\s*</section>)'
    # Since the masonry-grid has </div> inside it (for each image), .*? will match up to the first </div> which is just the first image!
    # Ah! `.*?</div>` will match the FIRST closing div.
    # I need to match everything up to `</div>\s*</div>\s*</section>` instead!
    
    pattern = rf'(<section id="{sec_id}".*?<div class="masonry-grid">.*?)(\s*</div>\s*</div>\s*</section>)'
    # Wait, the inner images are inside the masonry grid. The masonry grid ends right before `</div>\n </div>\n </section>`.
    # Let's just insert the button BEFORE `</div>\s*</section>`.
    
    # So `</div>\s*</section>` is the container closing. The one before it is the masonry-grid closing.
    # Actually, we can replace `</div>\s*</div>\s*</section>` with `</div>\n {btn} \n</div>\n</section>`
    pattern2 = rf'(<section id="{sec_id}".*?)(\s*</div>\s*</div>\s*</section>)'
    content = re.sub(pattern2, rf'\g<1>\n</div>{btn}</div>\n</section>', content, flags=re.DOTALL)

with open(index_file, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated HTML buttons")
