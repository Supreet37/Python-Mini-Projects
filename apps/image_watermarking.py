import os
from PIL import Image, ImageDraw, ImageFont

def watermark_photo(input_image_path, watermark_path, output_image_path, position='bottom-right', opacity=128):
    """
    Add watermark to an image
    
    Args:
        input_image_path: Path to original image
        watermark_path: Path to watermark image or text
        output_image_path: Path to save watermarked image
        position: 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'
        opacity: 0-255 for watermark opacity (only for image watermarks)
    """
    
    try:
        # Open base image
        base_image = Image.open(input_image_path).convert('RGBA')
        base_width, base_height = base_image.size
        
        # Check if watermark is text or image
        if watermark_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Image watermark
            watermark = Image.open(watermark_path).convert('RGBA')
            
            # Resize watermark to 15% of base image width (more reasonable)
            watermark_width = int(base_width * 0.15)
            watermark_height = int(watermark.height * (watermark_width / watermark.width))
            watermark = watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)
            
            # Adjust opacity
            if opacity < 255:
                watermark.putalpha(opacity)
            
            # Calculate position
            padding = 20
            if position == 'top-left':
                pos = (padding, padding)
            elif position == 'top-right':
                pos = (base_width - watermark_width - padding, padding)
            elif position == 'bottom-left':
                pos = (padding, base_height - watermark_height - padding)
            elif position == 'bottom-right':
                pos = (base_width - watermark_width - padding, base_height - watermark_height - padding)
            elif position == 'center':
                pos = (base_width // 2 - watermark_width // 2, base_height // 2 - watermark_height // 2)
            else:
                pos = (base_width - watermark_width - padding, base_height - watermark_height - padding)
            
            # Create transparent layer and composite
            transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
            transparent.paste(watermark, pos, watermark)
            watermarked = Image.alpha_composite(base_image, transparent)
            
        else:
            # Text watermark
            draw = ImageDraw.Draw(base_image)
            
            try:
                # Try to load a font, fallback to default
                font_size = int(base_width * 0.05)
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Calculate text size and position
            text = watermark_path
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            padding = 20
            if position == 'bottom-right':
                pos = (base_width - text_width - padding, base_height - text_height - padding)
            elif position == 'bottom-left':
                pos = (padding, base_height - text_height - padding)
            elif position == 'top-right':
                pos = (base_width - text_width - padding, padding)
            elif position == 'top-left':
                pos = (padding, padding)
            else:
                pos = (base_width // 2 - text_width // 2, base_height - text_height - padding)
            
            # Draw text with semi-transparent white
            draw.text(pos, text, fill=(255, 255, 255, opacity), font=font)
            watermarked = base_image
        
        # Save result
        if output_image_path.lower().endswith('.jpg') or output_image_path.lower().endswith('.jpeg'):
            watermarked = watermarked.convert('RGB')
        
        watermarked.save(output_image_path, optimize=True, quality=95)
        print(f"Saved: {output_image_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")
        return False

def main():
    print("Image Watermarking Tool")
    print("-" * 30)
    
    folder = input("Enter folder path with images: ").strip()
    watermark = input("Enter watermark (image path or text): ").strip()
    
    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        return
    
    if not os.path.exists(watermark) and not watermark.endswith(('.png', '.jpg', '.jpeg')):
        # Treat as text watermark
        print(f"Using text watermark: '{watermark}'")
    
    # Create output directory
    output_dir = os.path.join(folder, "watermarked")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get position preference
    print("\nWatermark positions:")
    print("1. Bottom-right (default)")
    print("2. Bottom-left")
    print("3. Top-right")
    print("4. Top-left")
    print("5. Center")
    
    pos_choice = input("Choose position (1-5): ").strip()
    positions = {
        '1': 'bottom-right',
        '2': 'bottom-left',
        '3': 'top-right',
        '4': 'top-left',
        '5': 'center'
    }
    position = positions.get(pos_choice, 'bottom-right')
    
    # Process images
    supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    processed = 0
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(supported_formats):
            output_path = os.path.join(output_dir, filename)
            if watermark_photo(file_path, watermark, output_path, position):
                processed += 1
    
    print(f"\nCompleted! Processed {processed} images. Output saved to: {output_dir}")

if __name__ == "__main__":
    main()