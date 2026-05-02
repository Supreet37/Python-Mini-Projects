from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import os
import sys

def setup_driver():
    """Setup Chrome driver with options"""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Try to find ChromeDriver in PATH
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Error: ChromeDriver not found. {e}")
        print("\nPlease install ChromeDriver:")
        print("1. Download from: https://chromedriver.chromium.org/")
        print("2. Add to PATH or place in script directory")
        return None

def scroll_and_load_comments(driver, max_scrolls=10):
    """Scroll to load more comments"""
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    for scroll_count in range(max_scrolls):
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        
        # Wait for new comments to load
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
        print(f"Scrolled {scroll_count + 1}/{max_scrolls} - Loaded more comments")

def scrape_youtube_comments(video_url, max_comments=100):
    """Scrape comments from YouTube video"""
    driver = setup_driver()
    if not driver:
        return []
    
    comments_data = []
    
    try:
        print(f"Loading video: {video_url}")
        driver.get(video_url)
        time.sleep(3)
        
        # Wait for comments section
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "comments"))
            )
        except:
            print("Could not find comments section")
        
        # Scroll to load comments
        print("Loading comments...")
        scroll_and_load_comments(driver, max_scrolls=5)
        
        # Find comment elements with new Selenium syntax
        username_elements = driver.find_elements(By.CSS_SELECTOR, "#author-text span")
        comment_elements = driver.find_elements(By.CSS_SELECTOR, "#content-text")
        
        print(f"Found {len(username_elements)} comments")
        
        # Collect comments
        for username, comment in zip(username_elements, comment_elements):
            if len(comments_data) >= max_comments:
                break
                
            comments_data.append({
                'Author': username.text.strip(),
                'Comment': comment.text.strip()
            })
        
        print(f"Collected {len(comments_data)} comments")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        driver.quit()
    
    return comments_data

def save_to_csv(comments, filename="youtube_comments.csv"):
    """Save comments to CSV file"""
    if not comments:
        print("No comments to save")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Author', 'Comment']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comments)
    
    print(f"Saved {len(comments)} comments to {filename}")

def main():
    print("\n" + "="*50)
    print("YOUTUBE COMMENT SCRAPER")
    print("="*50)
    
    # Get video URL
    video_url = input("\nEnter YouTube video URL: ").strip()
    
    if not video_url:
        print("Error: Please enter a valid URL")
        return
    
    # Get comment limit
    try:
        max_comments = int(input("Maximum comments to scrape (default 100): ").strip() or 100)
    except:
        max_comments = 100
    
    # Scrape comments
    comments = scrape_youtube_comments(video_url, max_comments)
    
    # Save to CSV
    if comments:
        save_to_csv(comments)
        print(f"\n✓ Successfully scraped {len(comments)} comments")
        
        # Preview first 5 comments
        print("\n--- Preview (first 5 comments) ---")
        for i, comment in enumerate(comments[:5], 1):
            print(f"{i}. {comment['Author']}: {comment['Comment'][:50]}...")
    else:
        print("No comments were scraped. Check the URL and try again.")

if __name__ == "__main__":
    main()