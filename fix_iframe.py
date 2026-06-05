import os
import re

base_dir = r"e:\AI_AGent\web-wedding"
index_file = os.path.join(base_dir, "index.html")

with open(index_file, "r", encoding="utf-8") as f:
    content = f.read()

# Add loading="lazy" to iframes if missing
content = re.sub(r'<iframe(?!.*?loading="lazy")', r'<iframe loading="lazy"', content)

with open(index_file, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated iframes")
