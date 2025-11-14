import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import re
from datetime import datetime

# --- Configuration ---
# 1. Choose a specific iPhone ASIN (e.g., iPhone 15, 128GB, Black)
TARGET_ASIN = "B0CHX1W1XY" # Example ASIN for iPhone 14
TARGET_URL = f"https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX1W1XY/ref=sr_1_3?crid=1FB9XIY8MPM7G&dib=eyJ2IjoiMSJ9.8-aKrERwPzdGyJWfWOa56HVaQ0finrCMh_nNUxQ9BYyGTrZaFQyF0HCto_wNjctmlvl_v4eRHG0bLVddYEDb2Jfh76i2tU9ewVXonOZzkAp2MFXMNArr3QwzLmoZNSNbg3KcyY1akG3T0jIywx6-K6994Fc8SBn7zf_L8DOqyLOyHNpuAzr3O-DvUrzDDpyudc97UxSCXNe9JOMNw0ksavPtMOdhPC4pz7MyAhFeSc4.czjcnt_KK3AiqJYPsq4n-oFFNb55yQ4X4yphEjgeSqU&dib_tag=se&keywords=iPhone%2B14&qid=1763059180&sprefix=iphone%2B14%2Caps%2C432&sr=8-3&th=1{TARGET_ASIN}"
RAW_DATA_PATH = os.path.join("01_Data", "01_Raw", "raw_product_data.csv")

# Standard User-Agent to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

# NOTE: CSS Selectors are based on typical Amazon HTML IDs/Classes and must be verified.
SELECTORS = {
    'product_name': '#productTitle',
    'brand': 'a#bylineInfo',
    'price': 'span.a-price-whole',
    'mrp': 'span.a-text-price .a-offscreen', # Full price that is often crossed out
    'stock_status': '#availability span.a-size-medium',
    'rating': 'span#acrCustomerReviewText', # Link text containing review count
    'reviews_count': 'span#acrCustomerReviewText', # Link text containing review count
    'seller_name': 'div#bylineInfo_feature_div a.a-link-normal', # Primary seller info
    'seller_link': 'div#bylineInfo_feature_div a.a-link-normal',
    'reviews_link': '#dp-summary-see-all-reviews',
}
# ---------------------

def fetch_page(url, headers):
    """Fetches the HTML content."""
    print(f"Fetching: {url}...")
    try:
        time.sleep(3) # Respectful delay
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {url}: {e}")
        return None

def parse_product_page(soup, asin, url):
    """Parses all required fields from the Beautiful Soup object."""
    data = {}

    # Helper function to safely extract text
    def safe_get_text(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else "N/A"

    # Helper function to extract price from a hidden span (often used for MSRP/MRP)
    def safe_get_offscreen_price(selector):
        el = soup.select_one(selector)
        if el:
            # Clean and return the price text (e.g., "₹ 79,900")
            return el.get_text(strip=True).replace('₹', '').replace(',', '')
        return "N/A"

    # --- Data Collection ---
    data["Product_Name"] = safe_get_text(SELECTORS['product_name'])
    data["Product_ASIN"] = asin
    data["Brand"] = safe_get_text(SELECTORS['brand'])
    data["Price"] = safe_get_text(SELECTORS['price']).replace(',', '').replace('.', '') # Current primary price
    
    # MRP/MSRP (Often found in a specific offscreen span)
    mrp_raw = safe_get_offscreen_price(SELECTORS['mrp'])
    data["MRP"] = mrp_raw

    # Stock Status
    data["Stock_Status"] = safe_get_text(SELECTORS['stock_status'])

    # Rating and Review Count
    reviews_count_text = safe_get_text(SELECTORS['reviews_count'])
    
    # Extract rating value from the title attribute of the star element (Requires specific selector)
    rating_el = soup.find('i', class_=re.compile(r'a-icon-star-small'))
    data["Rating"] = rating_el.get_text(strip=True).split(' ')[0] if rating_el else "N/A"
    
    # Extract review count (e.g., '10,000 ratings')
    data["Reviews"] = re.search(r'([\d,]+)', reviews_count_text).group(1) if re.search(r'([\d,]+)', reviews_count_text) else "N/A"

    # Seller Information
    seller_el = soup.select_one(SELECTORS['seller_name'])
    data["Seller"] = seller_el.get_text(strip=True) if seller_el else "N/A"

    # Links and Timestamp
    data["Product_Link"] = url
    data["Reviews_Link"] = url + "#customerReviews" # Standard Amazon review section anchor
    data["Scraped_At"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Discount Calculation (requires both Price and MRP to be numerical)
    try:
        price_num = float(data["Price"].split('.')[0].replace(',', ''))
        mrp_num = float(data["MRP"].split('.')[0].replace(',', ''))
        data["Discount"] = f"{((mrp_num - price_num) / mrp_num) * 100:.2f}%" if mrp_num > price_num else "0%"
    except (ValueError, AttributeError):
        data["Discount"] = "N/A"
    
    # Clean up the final Price and MRP fields
    data["Price"] = data["Price"].split('.')[0].replace(',', '')
    data["MRP"] = data["MRP"].split('.')[0].replace(',', '')

    return data

def scrape_and_save():
    """Main method to execute scraping and saving."""
    html_content = fetch_page(TARGET_URL, HEADERS)
    
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Parse all data points
        product_data = parse_product_page(soup, TARGET_ASIN, TARGET_URL)
        
        # Save data
        if product_data:
            df = pd.DataFrame([product_data])
            
            # Check if file exists to decide whether to write headers
            file_exists = os.path.exists(RAW_DATA_PATH)
            df.to_csv(RAW_DATA_PATH, index=False, mode='a', header=not file_exists)
            print(f"Data saved successfully to: {RAW_DATA_PATH}")

if __name__ == "__main__":
    scrape_and_save()