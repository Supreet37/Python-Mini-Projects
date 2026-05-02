import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import time
import hashlib

def get_image_links(url):
    """Extract all image URLs from a webpage"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        img_links = []
        
        # Find all img tags
        for img in soup.find_all('img'):
            img_url = img.get('src') or img.get('data-src')  # Check lazy-loaded images
            if img_url:
                # Convert relative URLs to absolute
                img_url = urljoin(url, img_url)
                img_links.append(img_url)
        
        # Remove duplicates
        img_links = list(dict.fromkeys(img_links))
        print(f"Found {len(img_links)} unique images")
        return img_links
    
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return []

def download_image(img_url, output_folder, index):
    """Download a single image"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(img_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Get file extension from URL or content-type
        content_type = response.headers.get('content-type', '')
        if 'jpeg' in content_type or 'jpg' in content_type:
            extension = '.jpg'
        elif 'png' in content_type:
            extension = '.png'
        elif 'gif' in content_type:
            extension = '.gif'
        elif 'webp' in content_type:
            extension = '.webp'
        else:
            # Try to get from URL
            parsed = urlparse(img_url)
            path = parsed.path
            if '.' in path:
                extension = os.path.splitext(path)[1]
                if extension.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
                    extension = '.jpg'
            else:
                extension = '.jpg'
        
        # Create filename
        filename = f"image_{index:04d}{extension}"
        filepath = os.path.join(output_folder, filename)
        
        # Save image
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Downloaded: {filename} ({len(response.content)} bytes)")
        return True
        
    except Exception as e:
        print(f"✗ Failed to download {img_url[:50]}...: {e}")
        return False

def download_all_images(url, output_folder="downloaded_images"):
    """Download all images from a webpage"""
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    print(f"Saving images to: {output_folder}")
    
    # Get all image links
    print(f"\nFetching images from: {url}")
    img_links = get_image_links(url)
    
    if not img_links:
        print("No images found on the page")
        return
    
    # Download images
    print(f"\nStarting download of {len(img_links)} images...")
    successful = 0
    
    for i, img_url in enumerate(img_links, 1):
        print(f"\n[{i}/{len(img_links)}] Downloading...")
        if download_image(img_url, output_folder, i):
            successful += 1
        time.sleep(0.5)  # Small delay to be respectful to server
    
    print(f"\n{'='*50}")
    print(f"DOWNLOAD COMPLETE!")
    print(f"✓ Successfully downloaded: {successful}/{len(img_links)} images")
    print(f"📁 Saved to: {os.path.abspath(output_folder)}")
    print(f"{'='*50}")

def main():
    print("\n" + "="*50)
    print("WEBPAGE IMAGE DOWNLOADER")
    print("="*50)
    
    # Get URL
    url = input("\nEnter webpage URL: ").strip()
    
    if not url:
        print("Error: Please enter a valid URL")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Get output folder name
    default_folder = "downloaded_images"
    folder = input(f"Output folder name [{default_folder}]: ").strip()
    if not folder:
        folder = default_folder
    
    # Start downloading
    try:
        download_all_images(url, folder)
    except KeyboardInterrupt:
        print("\n\n⚠ Download interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()