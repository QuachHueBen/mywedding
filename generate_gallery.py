import os
import re

base_dir = r"e:\AI_AGent\web-wedding"
images_dir = os.path.join(base_dir, "images")
index_file = os.path.join(base_dir, "index.html")

def get_image_tags(folder_name):
    folder_path = os.path.join(images_dir, folder_name)
    tags = []
    if os.path.exists(folder_path):
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        for f in files:
            tags.append(f'<div class="grid-item"><img src="images/{folder_name}/{f}" alt="{folder_name} image" loading="lazy" onclick="openLightbox(this)"></div>')
    return "\n                ".join(tags)

album_tags = get_image_tags("ALBUM")
nhatrai_tags = get_image_tags("NHATRAI")
nhagai_tags = get_image_tags("NHAGAI")

with open(index_file, "r", encoding="utf-8") as f:
    content = f.read()

def replace_grid(content, section_id, tags):
    pattern = rf'(<section id="{section_id}".*?<div class="masonry-grid">).*?(</div>\s*</div>\s*</section>)'
    return re.sub(pattern, lambda m: m.group(1) + "\n                " + tags + "\n            " + m.group(2), content, flags=re.DOTALL)

content = replace_grid(content, "album-studio", album_tags)
content = replace_grid(content, "album-nhatrai", nhatrai_tags)
content = replace_grid(content, "album-nhagai", nhagai_tags)

with open(index_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated index.html with {max(0, len(album_tags.split('<div'))-1)} ALBUM images, {max(0, len(nhatrai_tags.split('<div'))-1)} NHATRAI images, and {max(0, len(nhagai_tags.split('<div'))-1)} NHAGAI images.")
