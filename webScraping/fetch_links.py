import requests as rq
from bs4 import BeautifulSoup
import sys

def fetch_links(url):
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = rq.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        
        for link in soup.find_all("a", href=True):
            href = link['href']
            # Convert relative URLs to absolute
            if href.startswith('/'):
                href = url.rstrip('/') + href
            elif not href.startswith(('http://', 'https://')):
                href = url.rstrip('/') + '/' + href
            links.append(href)
        
        # Remove duplicates while preserving order
        unique_links = []
        seen = set()
        for link in links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        return unique_links
    
    except rq.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def save_links(links, filename="myLinks.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Total links found: {len(links)}\n")
        f.write("="*50 + "\n\n")
        for i, link in enumerate(links, 1):
            f.write(f"{i}. {link}\n")
    
    print(f"Saved {len(links)} links to {filename}")
    
    # Also show first 10 in console
    print("\nFirst 10 links:")
    for i, link in enumerate(links[:10], 1):
        print(f"{i}. {link}")

def main():
    url = input("Enter website URL: ")
    print(f"Fetching links from {url}...")
    
    links = fetch_links(url)
    
    if links:
        save_links(links)
    else:
        print("No links found or unable to fetch the page.")

if __name__ == "__main__":
    main()