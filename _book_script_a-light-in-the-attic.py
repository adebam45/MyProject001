import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
# import os

def scrape_book_details(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract book details
    title = soup.find('div', class_='product_main').h1.text.strip()
    price = soup.find('p', class_='price_color').text.strip()
    availability = soup.find('p', class_='instock availability').text.strip()
    rating = soup.find('p', class_='star-rating')['class'][1]


    # Extract product category

    breadcrumb=soup.find('ul', class_='breadcrumb')
    category=breadcrumb.find_all('li')[2].a.text.strip()

    # Extract product description
    description_tag = soup.find('div', id='product_description')
    if description_tag:
        description = description_tag.find_next_sibling('p').text.strip()
    else:
        description = "No description available"

    # Extract image URL
    image_tag = soup.find('div', class_='item active').img
    relative_image_url = image_tag['src']
    image_url = urljoin(url, relative_image_url)

    # Extract product info from the table
    table = soup.find('table', class_='table table-striped')
    product_info = {}
    for row in table.find_all('tr'):
        key = row.th.text.strip()
        value = row.td.text.strip()
        product_info[key] = value

    # Convert prices to USD (example conversion rate)
    exchange_rate = 1.12
    for key in ['Price (excl. tax)', 'Price (incl. tax)', 'Tax']:
        if key in product_info:
            pound_value = float(product_info[key].replace('£', '').strip())
            dollar_value = round(pound_value * exchange_rate, 2)
            product_info[f"{key} (USD)"] = f"${dollar_value}"

    # Compile all book data
    book_data = {
        'Title': title,
        'Category': category,
        'Price': price,
        'Availability': availability,
        'Rating': rating,
        'Description': description,
        'Image URL': image_url
    }

    # Add product info fields to book_data
    book_data.update(product_info)

    return book_data


# Script to pull and save as csv
def save_to_csv(book_data, filename='book_details.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=book_data.keys())
        writer.writeheader()
        writer.writerow(book_data)
    print(f"Book details saved to '{filename}'")


# The code to run the main program 
def main(): 
    book_url = input("Enter the URL from book website: ").strip()
    try:
        book_data = scrape_book_details(book_url)
        save_to_csv(book_data)
    except Exception as e:
        print(f"Failed to scrape the book: {e}")

if __name__ == "__main__":
    main()