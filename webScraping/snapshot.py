import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import time

def take_website_screenshot(url, output_file="screenshot.png", width=None, height=None):
    """
    Take screenshot of a website
    """
    driver = None
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Add user agent to avoid detection
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Initialize driver
        try:
            # Try to find ChromeDriver in PATH
            driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException:
            # Try using Service object
            print("ChromeDriver not found in PATH. Trying common locations...")
            possible_paths = [
                './chromedriver.exe',
                './chromedriver',
                '../chromedriver.exe',
                'C:/chromedriver/chromedriver.exe'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    service = Service(path)
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    break
            
            if not driver:
                print("\n❌ ChromeDriver not found!")
                print("\nTo fix:")
                print("1. Download ChromeDriver from: https://chromedriver.chromium.org/")
                print("2. Add it to your PATH or place it in the script directory")
                return False
        
        # Navigate to URL
        print(f"Loading website: {url}")
        driver.get(url)
        time.sleep(2)  # Wait for page to load
        
        # Set custom window size if specified
        if width and height:
            driver.set_window_size(width, height)
        
        # Get full page dimensions
        page_width = driver.execute_script('return document.body.scrollWidth')
        page_height = driver.execute_script('return document.body.scrollHeight')
        
        # Set window size to full page
        driver.set_window_size(page_width, page_height)
        
        # Take screenshot
        driver.save_screenshot(output_file)
        
        print(f"\n✓ Screenshot saved: {output_file}")
        print(f"  Dimensions: {page_width}x{page_height}")
        print(f"  File size: {os.path.getsize(output_file) / 1024:.2f} KB")
        return True
        
    except WebDriverException as e:
        print(f"\n❌ WebDriver error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Chrome browser is installed")
        print("2. Download matching ChromeDriver version")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()

def main():
    print("\n" + "="*50)
    print("WEBSITE SCREENSHOT TOOL")
    print("="*50)
    
    # Get URL from command line or input
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("\nEnter website URL: ").strip()
    
    if not url:
        print("Error: Please provide a URL")
        print("Usage: python script.py https://example.com")
        return
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"screenshot_{timestamp}.png"
    
    filename = input(f"Output filename [{default_filename}]: ").strip()
    if not filename:
        filename = default_filename
    if not filename.endswith(('.png', '.jpg', '.jpeg')):
        filename += '.png'
    
    # Optional custom dimensions
    custom_size = input("Custom dimensions (width,height) or press Enter for full page: ").strip()
    width = height = None
    if custom_size:
        try:
            width, height = map(int, custom_size.split(','))
            print(f"Using custom dimensions: {width}x{height}")
        except:
            print("Invalid dimensions. Using full page.")
    
    # Take screenshot
    print(f"\n📸 Taking screenshot of: {url}")
    success = take_website_screenshot(url, filename, width, height)
    
    if success:
        print(f"\n✅ Screenshot created successfully!")
    else:
        print(f"\n❌ Failed to create screenshot")

if __name__ == "__main__":
    main()