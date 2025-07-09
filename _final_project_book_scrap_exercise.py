# Importing required libraries

import requests  #Used to make HTTP requests
from bs4 import BeautifulSoup #Used to parsed HTML content
from urllib.parse import urljoin, urlparse  #Used to handle and join URLs
import csv  #Used to write data to CSV files
import os  #Used for interacting with operating system (file creation)
import wget  # For downloading images from URL


# Function definition: encapsulates logic for fetching and parsing a webpage
def get_soup(url):
    response = requests.get(url)  #Makes a GET request to the provided URL
    response.raise_for_status()  #Raises an exception for HTTP errors(i.e, 404 etc)
    return BeautifulSoup(response.content, 'html.parser') #Parses HTML content into a soup object

# Creating a directory for saving images
image_folder = 'book_images'  #Fuction for folder name as a string
os.makedirs(image_folder, exist_ok=True)  #Creating the folder if it doesnt already exists

# Creating a directory for saving CSV files
output_folder = 'book_data'
os.makedirs(output_folder, exist_ok=True)


# Function to scrape all book-level details
# Arguments: book_url - URL of individual book
#            base_url - Root URL of site
#            category_folder - Name of category folder for image organization
def scrape_book_details(book_url, base_url, category_folder):
    soup = get_soup(book_url)  #Reuses soup function to get HTML tree

# Extracting book metadata from specific HTML tags
    title = soup.find('div', class_='product_main').h1.text.strip()  #Strip to get title
    price = soup.find('p', class_='price_color').text.strip()        #Strip price in GBP
    availability = soup.find('p', class_='instock availability').text.strip()   #Availability status

# Rating is extracted from class attribute, which embeds rating
    rating_tag = soup.find('p', class_='star-rating')
    rating = rating_tag['class'][1] if rating_tag else 'Not rated'

# Extract category from breadcrumb trail
    breadcrumbs = soup.select('ul.breadcrumb li a')
    category = breadcrumbs[2].text.strip() if len(breadcrumbs) > 2 else 'Unknown'

# Try to extract book description
    description = "No description available"
    description_div = soup.find('div', id='product_description')
    if description_div:
        next_p = description_div.find_next_sibling('p')   #Get paragraph after description header
        if next_p:
            description = next_p.text.strip()

# Handling image download logic
    image_url = ''
    image_filename = ''
    image_tag = soup.find('div', class_='item active')
    if image_tag:
        img = image_tag.find('img')
        if img and img.get('src'):
            image_url = urljoin(book_url, img['src'])     #Joins relative path to absolute URL
            image_filename = os.path.basename(image_url)  #Extracts filename from path
            image_path = os.path.join(image_folder, category_folder, image_filename)   #Full path to save image
            os.makedirs(os.path.join(image_folder, category_folder), exist_ok=True)

            try:
                wget.download(image_url, out=image_path)     #Downloads image to path
                print(f"\n Downloaded image: {image_filename}")
            except Exception as e:
                print(f"\n Failed to download image: {e}")
                image_filename = 'Download failed'

# Extracts all rows from product information table
    product_info = {}
    table = soup.find('table', class_='table table-striped')
    if table:
        for row in table.find_all('tr'):
            key = row.th.text.strip()
            value = row.td.text.strip()
            product_info[key] = value    #Populating dictionary with the book info

# Currency conversion from GBP to USD
    exchange_rate = 1.12
    for key in ['Price (excl. tax)', 'Price (incl. tax)', 'Tax']:
        if key in product_info:
            try:
                pound_value = float(product_info[key].replace('\u00a3', '').strip())
                usd_value = round(pound_value * exchange_rate, 2)
                product_info[f"{key} (USD)"] = f"${usd_value}"
            except:
                product_info[f"{key} (USD)"] = "N/A"

# Return a dictionary with all extracted book information
    return {
        'Title': title,
        'Category': category,
        'Price (GBP)': price,
        'Availability': availability,
        'Rating': rating,
        'Description': description,
        'Image URL': image_url,
        'Image Filename': image_filename,
        **product_info     #Merge in product info key-values
    }


# Function to scrape all books in a category page and paginate if needed
def scrape_category_books(category_url):
    books = []    #List to collect book dictionaries 

    parsed_url = urlparse(category_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"   #Extract scheme and domain

    soup = get_soup(category_url) 
    heading = soup.find('div', class_='page-header action').h1
    category_name = heading.text.strip() if heading else 'Unknown'

    while category_url:
        print(f"Scraping page: {category_url}")
        soup = get_soup(category_url)
        book_links = soup.select('h3 a')   #All book anchor tags

        for link in book_links:
            book_relative_url = link['href'].replace('../../../', 'catalogue/')
            book_url = urljoin(base_url, book_relative_url)   #Appends each book dict to list
            try:
                book_data = scrape_book_details(book_url, base_url, category_name)
                books.append(book_data)
            except Exception as e:
                print(f"Failed to scrape the book: {e}")

        next_button = soup.select_one('li.next a')    #Check for pagination and navigate to the next page if necessary
        if next_button:
            next_page = next_button['href']
            category_url = urljoin(category_url, next_page)
        else:
            category_url = None

    return books, category_name


# Function to save book data to a CSV file
def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return

    file_path = os.path.join(output_folder, filename)
    with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())    #Uses first dict to define header
        writer.writeheader()     #Write column names                      
        writer.writerows(data)   #Writes each book dictionary as a row
    print(f"Saved {len(data)} books to {file_path}")


# Entry point function for user interaction and full site scraping
def main():
    home_url = input("Enter the base URL (e.g.. Bookscrap.com): ").strip()
    main_soup = get_soup(home_url)
    categories = main_soup.select('div.side_categories ul li ul li a')     #Finding all categories 

    for cat in categories:
        category_relative_url = cat['href']
        category_url = urljoin(home_url, category_relative_url)

        try:
            books, category_name = scrape_category_books(category_url)
            csv_filename = f"{category_name.lower().replace(' ', '_')}.csv"
            save_to_csv(books, csv_filename)
        except Exception as e:
            print(f"Failed to scrape category {category_url}: {e}")


#Ensure main runs only if this script is executed directly
if __name__ == "__main__":
    main()
