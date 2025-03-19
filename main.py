import re
import sqlite3
from books_to_scrape import *

# Start of code from last week
# Scrape the fiction page
BASE_URL = "http://books.toscrape.com/catalogue/category/books/fiction_10/page-{}.html"
books = scrape_pages("https://books.toscrape.com/catalogue/category/books/fiction_10/index.html", 1, 4)

# Connect to the books database
connection = sqlite3.connect('books.db')
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS books")
cursor.execute('''CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price REAL,
    rating INTEGER,
    availability TEXT,
    genre TEXT
    );
''')

# Insert the values into the books database
for book in books:
    cursor.execute('''
        INSERT INTO books (title, price, rating, availability, genre)
        VALUES (?, ?, ?, ?, ?)
    ''', (book[0], book[1], book[2], book[3], book[4]))

# Commit the values
connection.commit()

# End of code from last week