from tqdm import tqdm
from PIL import Image
import os
import sys

def resize_image(size, image_path, output_dir):
    """Resize a single image"""
    try:
        with Image.open(image_path) as img:
            # Handle different Pillow versions (ANTIALIAS deprecated)
            try:
                # For newer Pillow versions (10.0.0+)
                img.thumbnail(size, Image.LANCZOS)
            except AttributeError:
                # For older Pillow versions
                img.thumbnail(size, Image.ANTIALIAS)
            
            # Save resized image
            output_path = os.path.join(output_dir, os.path.basename(image_path))
            img.save(output_path, optimize=True, quality=85)
            return True
    except Exception as e:
        print(f"\nError resizing {image_path}: {e}")
        return False

def main():
    print("\n" + "="*50)
    print("BULK IMAGE RESIZER WITH PROGRESS BAR")
    print("="*50)
    
    # Get input path
    path = input("\nEnter folder path with images: ").strip()
    
    if not os.path.exists(path):
        print(f"Error: Path '{path}' not found")
        return
    
    # Get size
    size_input = input("Enter size (width,height) e.g., 800,600: ").strip()
    try:
        width, height = map(int, size_input.split(','))
        size = (width, height)
    except:
        print("Invalid size format. Using 800x600")
        size = (800, 600)
    
    # Create output directory
    output_dir = os.path.join(path, "resized")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all images
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    images = []
    
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in image_extensions:
            images.append(file)
    
    if not images:
        print(f"No images found in '{path}'")
        return
    
    print(f"\nFound {len(images)} images to resize")
    print(f"Resizing to {size[0]}x{size[1]} pixels")
    print(f"Output folder: {output_dir}\n")
    
    # Process with progress bar
    successful = 0
    for image in tqdm(images, desc="Resizing images", unit="img"):
        if resize_image(size, os.path.join(path, image), output_dir):
            successful += 1
    
    print(f"\n✓ Complete! Resized {successful}/{len(images)} images")
    print(f"Output saved to: {output_dir}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Process interrupted by user")
        sys.exit(0)