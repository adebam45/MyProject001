# Importing the libraries necessary for web scrapping, Parsing HTML and navigating the HTML tree
# URLjoin and URLparse, used for URL manipulation etc.
# csv is used to write structured data to csv
# wget download images and files using URL

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import os
import wget  #Import for downloading images

# Functions to fetch HTML and parse into beautiful soup object
def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')

# Create folder called 'book_image' to save images
image_folder = 'book_images'
os.makedirs(image_folder, exist_ok=True)


# Create function is used to scrap book details (i.e., title, price, ratings etc)
def scrape_book_details(book_url, base_url):
    soup = get_soup(book_url)


# The tags ('div', 'p') are used to extract product information(title, price, availability and ratings)
    title = soup.find('div', class_='product_main').h1.text.strip()
    price = soup.find('p', class_='price_color').text.strip()
    availability = soup.find('p', class_='instock availability').text.strip()
    
    rating_tag = soup.find('p', class_='star-rating')
    rating = rating_tag['class'][1] if rating_tag else 'Not rated'

# The line functions are used to get book category from breadcrumbs
    breadcrumbs = soup.select('ul.breadcrumb li a')
    category = breadcrumbs[2].text.strip() if len(breadcrumbs) > 2 else 'Unknown'

# This function is used to scrap the description of the book
    description = "No description available"
    description_div = soup.find('div', id='product_description')
    if description_div:
        next_p = description_div.find_next_sibling('p')
        if next_p:
            description = next_p.text.strip()

# This function is use to scrap images and download book img
    image_url = ''
    image_filename = ''
    image_tag = soup.find('div', class_='item active')
    if image_tag:
        img = image_tag.find('img')
        if img and img.get('src'):
            image_url = urljoin(book_url, img['src'])
            image_filename = os.path.basename(image_url)
            image_path = os.path.join(image_folder, image_filename)

            try:
                wget.download(image_url, out=image_path)
                print(f"\n Downloaded image: {image_filename}")
            except Exception as e:
                print(f"\n Failed to download image: {e}")
                image_filename = 'Download failed'

    # Product Info table
    product_info = {}
    table = soup.find('table', class_='table table-striped')
    if table:
        for row in table.find_all('tr'):
            key = row.th.text.strip()
            value = row.td.text.strip()
            product_info[key] = value

    # Convert GBP to USD
    exchange_rate = 1.12
    for key in ['Price (excl. tax)', 'Price (incl. tax)', 'Tax']:
        if key in product_info:
            try:
                pound_value = float(product_info[key].replace('£', '').strip())
                usd_value = round(pound_value * exchange_rate, 2)
                product_info[f"{key} (USD)"] = f"${usd_value}"
            except:
                product_info[f"{key} (USD)"] = "N/A"

    return {
        'Title': title,
        'Category': category,
        'Price (GBP)': price,
        'Availability': availability,
        'Rating': rating,
        'Description': description,
        'Image URL': image_url,
        'Image Filename': image_filename,  #: Store image filename
        **product_info
    }

def scrape_category_books(category_url):
    books = []

    # Get base URL dynamically from user input
    parsed_url = urlparse(category_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"

    while category_url:
        print(f"Scraping page: {category_url}")
        soup = get_soup(category_url)
        book_links = soup.select('h3 a')

        for link in book_links:
            book_relative_url = link['href'].replace('../../../', 'catalogue/')
            book_url = urljoin(base_url, book_relative_url)
            try:
                book_data = scrape_book_details(book_url, base_url)
                books.append(book_data)
            except Exception as e:
                print(f"Failed to scrape the book: {e}")

        next_button = soup.select_one('li.next a')
        if next_button:
            next_page = next_button['href']
            category_url = urljoin(category_url, next_page)
        else:
            category_url = None

    return books

def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return

    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} books to {filename}")

def main():
    category_url = input("Enter the full category URL (e.g. mystery, poetry category): ").strip()
    try:
        books = scrape_category_books(category_url)
        save_to_csv(books, "mystery.csv")
    except Exception as e:
        print(f"Failed to scrape: {e}")

if __name__ == "__main__":
    main()
