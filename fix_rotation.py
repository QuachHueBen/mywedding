import os
from PIL import Image, ImageOps
import concurrent.futures

base_dir = r"e:\AI_AGent\web-wedding"
images_dir = os.path.join(base_dir, "images")
images_webp_dir = os.path.join(base_dir, "images_webp")

def main():
    if not os.path.exists(images_dir):
        print("Original images folder not found!")
        return

    tasks = []
    for root, dirs, files in os.walk(images_dir):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                src_path = os.path.join(root, f)
                rel_path = os.path.relpath(src_path, images_dir)
                base_name = os.path.splitext(rel_path)[0]
                dest_path = os.path.join(images_webp_dir, base_name + '.webp')
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                tasks.append((src_path, dest_path))

    def process_image(paths):
        src, dest = paths
        try:
            with Image.open(src) as img:
                # Correct EXIF orientation before doing anything else
                img = ImageOps.exif_transpose(img)
                
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
                
                # Overwrite existing webp
                img.save(dest, 'WEBP', quality=80)
        except Exception as e:
            print(f"Failed to process {src}: {e}")

    print(f"Reprocessing {len(tasks)} images to fix rotation...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        list(executor.map(process_image, tasks))
    
    print("All images fixed and converted to WebP!")

if __name__ == "__main__":
    main()
