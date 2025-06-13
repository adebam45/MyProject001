# Write your code here!
from bs4 import BeautifulSoup

with open ("C:/Users/ayoba/PycharmProjects/AyobamiPythonProject/MyProject001/P3/P3C2/statement/index.html", 'r', encoding='utf-8') as file:
    soup=BeautifulSoup(file, 'html.parser')

# Get the page title
page_title=soup.title.string

# Get the text inside the h1 tag
h1_text=soup.h1.string

# Extraction of the names and prices of the products in the list
products = soup.find_all('li')
products_list = []
for product in products:
    name = product.h2.string
    price = product.find('p', string=lambda s: 'Price' in s).string
    products_list.append((name, price))

# Extraction of the descriptions of the products in the list
descriptions_list = []
for product in products:
    description = product.find('p', string=lambda s: 'Description' in s).string
    descriptions_list.append(description)

# Step 2 : Displaying the extracted information
print("Title of the page :", page_title)
print("Text of the h1 tag :", h1_text)
print("Product list :", products_list)
print("List of product descriptions :", descriptions_list)

# Step 3 : Conversion of prices to dollars
for i, (name, price) in enumerate(products_list):
    euro_amount = price.split("€")[-1]
    euro_price = float(euro_amount)
    dollar_price = round(euro_price * 1.2, 2)
    products_list[i] = (name, f"${dollar_price}") # Dollar sign in front


# Step 4 : Displaying the new list with prices in dollars
print("List of products :", products_list)