from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import time
from urllib.parse import quote

def search_imdb_movie(title):
    """Search for a movie on IMDB and return rating and genre"""
    
    # Format the title for URL
    query = quote(title.lower())
    url = f"https://www.imdb.com/find?q={query}&s=tt&ttype=ft&ref_=fn_ft"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the first movie result
        result_table = soup.find('table', class_='findList')
        if not result_table:
            return None, None, None
        
        first_result = result_table.find('td', class_='result_text')
        if not first_result:
            return None, None, None
        
        # Get the movie link
        movie_link = first_result.find('a')
        if not movie_link:
            return None, None, None
        
        movie_url = 'https://www.imdb.com' + movie_link['href']
        exact_title = movie_link.text
        
        # Now get the movie page
        time.sleep(1)  # Be respectful to IMDB
        movie_response = requests.get(movie_url, headers=headers, timeout=10)
        movie_soup = BeautifulSoup(movie_response.content, 'html.parser')
        
        # Get rating
        rating_elem = movie_soup.find('div', {'data-testid': 'hero-rating-bar'})
        if rating_elem:
            rating_span = rating_elem.find('span', class_='sc-7ab21ed2-1')
            rating = rating_span.text if rating_span else 'N/A'
        else:
            rating = 'N/A'
        
        # Get genres
        genre_section = movie_soup.find('div', {'data-testid': 'genres'})
        if genre_section:
            genre_spans = genre_section.find_all('span', class_='ipc-chip__text')
            genres = ', '.join([g.text for g in genre_spans])
        else:
            genres = 'N/A'
        
        return exact_title, rating, genres
    
    except Exception as e:
        print(f"Error searching for '{title}': {e}")
        return None, None, None

def get_movies_from_folder(folder_path):
    """Get movie names from video files in a folder"""
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return []
    
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.m4v'}
    movies = []
    
    for file in os.listdir(folder_path):
        name, ext = os.path.splitext(file)
        if ext.lower() in video_extensions:
            # Clean up the name (remove quality indicators, year, etc.)
            clean_name = name.split('(')[0].split('[')[0].strip()
            movies.append(clean_name)
    
    return movies

def main():
    print("IMDB Movie Rating Scraper")
    print("-" * 40)
    
    # Option to either input movies manually or from folder
    choice = input("Enter '1' to input movie names manually, or '2' to scan a folder: ")
    
    movies = []
    
    if choice == '1':
        print("Enter movie names (one per line, empty line to finish):")
        while True:
            movie = input().strip()
            if not movie:
                break
            movies.append(movie)
    
    elif choice == '2':
        folder = input("Enter folder path containing movies: ")
        movies = get_movies_from_folder(folder)
        if not movies:
            print("No video files found in the folder.")
            return
        print(f"Found {len(movies)} movie files.")
    
    else:
        print("Invalid choice.")
        return
    
    # Scrape ratings
    names = []
    ratings = []
    genres = []
    
    print("\nFetching ratings from IMDB...")
    
    for i, movie in enumerate(movies, 1):
        print(f"Processing {i}/{len(movies)}: {movie}")
        name, rating, genre = search_imdb_movie(movie)
        
        if name:
            names.append(name)
            ratings.append(rating)
            genres.append(genre)
        else:
            names.append(movie)
            ratings.append('Not Found')
            genres.append('Not Found')
        
        # Be respectful to IMDB
        time.sleep(2)
    
    # Create and save dataframe
    df = pd.DataFrame({
        'Film Name': names,
        'Rating': ratings,
        'Genre': genres
    })
    
    output_file = 'film_ratings.csv'
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nResults saved to {output_file}")
    
    # Display summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()