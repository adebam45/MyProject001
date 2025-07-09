## Web Scraping Book Project - Unified README

This repository documents **three web scraping scripts** developed to extract book data from [BooksToScrape.com](https://books.toscrape.com). These scripts gather various metadata, download book cover images, and save the extracted data into CSV files.

---

###  Features

- Scrape details for one book, an entire book category, or the entire book website.
- Extracts structured information: title, price, availability, rating, category, description, image URL, UPC, and more.
- Converts prices from GBP to USD.
- Downloads book cover images.
- Saves data in structured `.csv` format.

---

###  Projects Overview

#### 1. **Single Book Scraper**

- Scrapes data from a **user-input URL** pointing to a specific book page.
- Outputs:
  - A single-row CSV file (`book_details.csv`)
  - No image download in this version

#### 2. **Category Book Scraper**

- Prompts the user to enter a URL for a category (e.g. poetry, mystery).
- Downloads:
  - Book data from all pages within the category
  - Book cover images (e.g., mystery_book_images)
  - Outputs CSV file (e.g., `poetry.csv`)

#### 3. **Full Book Site Scraper**

- Prompts for the base URL of the site (e.g., [https://books.toscrape.com](https://books.toscrape.com)).
- Automatically detects all categories and scrapes all books across them.
- Outputs:
  - One CSV file per category (saved in `book_data/`)
  - Images per book saved in `book_images/<category>/`

---

###  Technologies Used

- `Python`
- `requests` – HTTP requests
- `BeautifulSoup` – HTML parsing
- `csv` – Save structured data
- `os` – File system operations
- `urllib.parse` – URL handling
- `wget` – Image downloading

---

###  Project Structure

```
.
├── book_images/         # Folder containing downloaded images by category
├── book_data/           # Folder containing CSV files for each category
├── _book_script.py      # Single book scraper
├── _category_script.py  # Category scraper
├── _site_scraper.py     # Full site scraper
```

---

###  How to Run

1. **Clone the repository**

```
git clone https://github.com/your-username/book-scraper.git
cd book-scraper
```

2. **Install required packages**

```
pip install requests beautifulsoup4 wget
```

3. **Run a script**

```
 _book_script_a-light-in-the-attic.py        # Scrape one book
 _mystery_book_script.py                     # Scrape one category
 _final_project_book_scrap_exercise.py       # Scrape the full website
```

4. **Follow prompts** (enter URL when asked)

---

###  Output

- CSV files: book data with all fields and prices (GBP + USD)
- Folders with images for each category

---

###  Author

**Ayobami Adeyemo**\
Data Analyst
GitHub: [adebam45](https://github.com/adebam45)

---

###  Future Improvements

- Add pagination logging and progress bars
- Export as JSON or SQLite
- Enable scheduling via cron or task scheduler (Automation)
- Add filtering or analytics features on top of scraped data

