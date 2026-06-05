import os
import shutil
import re
from PIL import Image
import concurrent.futures

base_dir = r"e:\AI_AGent\web-wedding"
images_dir = os.path.join(base_dir, "images")
images_webp_dir = os.path.join(base_dir, "images_webp")
index_file = os.path.join(base_dir, "index.html")

def main():
    # 1. Create images_webp dir
    os.makedirs(images_webp_dir, exist_ok=True)

    # 2. Collect all tasks
    tasks = []
    if os.path.exists(images_dir):
        for root, dirs, files in os.walk(images_dir):
            for f in files:
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    src_path = os.path.join(root, f)
                    rel_path = os.path.relpath(src_path, images_dir)
                    # Create WebP extension path
                    base_name = os.path.splitext(rel_path)[0]
                    dest_path = os.path.join(images_webp_dir, base_name + '.webp')
                    
                    # Ensure destination folder exists
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    
                    tasks.append((src_path, dest_path))

    def process_image(paths):
        src, dest = paths
        if os.path.exists(dest):
            return  # Skip if already exists
        try:
            with Image.open(src) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                max_width = 1920
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_h = int(img.height * ratio)
                    
                    try:
                        resample_filter = Image.Resampling.LANCZOS
                    except AttributeError:
                        resample_filter = Image.ANTIALIAS
                    
                    img = img.resize((max_width, new_h), resample_filter)
                
                img.save(dest, 'WEBP', quality=80)
        except Exception as e:
            print(f"Failed to process {src}: {e}")

    print(f"Processing {len(tasks)} images...")
    
    # 3. Process images concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        list(executor.map(process_image, tasks))
    
    print("All images compressed and converted to WebP!")

    # 4. Update index.html to point to images_webp and .webp extensions
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # We need to replace src="images/ALBUM/image.jpg" with src="images_webp/ALBUM/image.webp"
        # First change images/ to images_webp/ in src attributes
        content = re.sub(r'src="images/', r'src="images_webp/', content)
        # Then change extensions to .webp
        content = re.sub(r'(src="images_webp/[^"]*?)(\.jpg|\.jpeg|\.png|\.gif)"', r'\1.webp"', content, flags=re.IGNORECASE)
        
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated HTML to use images_webp and .webp")

if __name__ == "__main__":
    main()
