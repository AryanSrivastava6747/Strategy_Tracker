import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from datetime import datetime

# --- Configuration ---
# Target ASIN from the previous scrape (Apple iPhone 15)
TARGET_ASIN = "B0CHX1W1XY" 

# The base URL template for the review section, including pagination
BASE_REVIEW_URL = f"https://www.amazon.in/product-reviews/{TARGET_ASIN}/ref=cm_cr_arp_d_paging_btm_next_1?ie=UTF8&reviewerType=all_reviews&pageNumber="

RAW_REVIEWS_PATH = os.path.join("01_Data", "01_Raw", "raw_reviews_data.csv")

# Setting a high limit (500 pages) to capture historical data.
MAX_PAGES = 500 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

# 🎯 FIXED SELECTORS based on user-provided HTML
SELECTORS = {
    # Fix: Changed from 'div' to 'li' with data-hook
    'review_card': 'li[data-hook="review"]', 
    'rating': 'i[data-hook="review-star-rating"] span.a-icon-alt', 
    'title': 'a[data-hook="review-title"] span',
    # Changed to use the most direct data-hook for the full text container
    'text': 'span[data-hook="review-body"]', 
    'date': 'span[data-hook="review-date"]',
}
# ---------------------

def fetch_page(url, headers):
    """Fetches the HTML content with error handling and delay."""
    print(f"Fetching: {url}")
    try:
        # Essential delay to prevent IP banning
        time.sleep(4) 
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {url}: {e}")
        return None

def parse_reviews(soup, reviews_list):
    """Parses individual reviews from a single page."""
    # Using the fixed selector
    review_cards = soup.select(SELECTORS['review_card'])
    
    if not review_cards:
        return False, "No review cards found on the page."

    for card in review_cards:
        rating_el = card.select_one(SELECTORS['rating'])
        title_el = card.select_one(SELECTORS['title'])
        text_el = card.select_one(SELECTORS['text'])
        date_el = card.select_one(SELECTORS['date'])
        
        # Extract and clean data
        review_rating = rating_el.get_text(strip=True).split(' ')[0] if rating_el else "N/A"
        review_title = title_el.get_text(strip=True) if title_el else "N/A"
        
        # Extracting text from the main review body span
        review_text = text_el.get_text(strip=True) if text_el else "N/A"
        
        # Cleaning the date string
        review_date_raw = date_el.get_text(strip=True) if date_el else "N/A"
        review_date = review_date_raw.split(" on ")[-1] if " on " in review_date_raw else review_date_raw
        
        reviews_list.append({
            'Product_ASIN': TARGET_ASIN,
            'Review_Title': review_title,
            'Review_Text': review_text,
            'Review_Rating': review_rating,
            'Review_Date_Raw': review_date,
            'Scraped_At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    return True, f"Scraped {len(review_cards)} reviews."

def scrape_all_reviews():
    """Iterates through review pages and collects all reviews."""
    all_reviews = []
    file_exists = os.path.exists(RAW_REVIEWS_PATH)

    for page_num in range(1, MAX_PAGES + 1):
        url = BASE_REVIEW_URL + str(page_num)
            
        # Stopping condition based on typical Amazon behavior
        if page_num > 100: 
            break
            
        html_content = fetch_page(url, HEADERS)
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            success, message = parse_reviews(soup, all_reviews)
            print(f"Page {page_num}: {message}")
            
            # Stop if no reviews are found
            if not success and page_num > 1:
                print(f"Exiting scrape loop (no more reviews). Total reviews collected: {len(all_reviews)}")
                break
            
            # Amazon often redirects page 10+ back to page 1 if page doesn't exist.
            # We need a better stop condition based on content, but this is the simplest for now.
        else:
            print(f"Stopping scrape due to page fetch failure on page {page_num}. Total collected: {len(all_reviews)}")
            break
            
    # Save all collected data
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_csv(RAW_REVIEWS_PATH, index=False, mode='a', header=not file_exists)
        print(f"\nTotal of {len(all_reviews)} reviews saved to: {RAW_REVIEWS_PATH}")
    else:
        print("\nNo reviews were successfully collected.")

if __name__ == "__main__":
    scrape_all_reviews()