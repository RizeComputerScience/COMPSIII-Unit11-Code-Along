import re
import sqlite3
from books_to_scrape import *
# Import and install pandas and matplotlib
import pandas as pd
import matplotlib.pyplot as plt

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

# Load Data from SQLite
query = "SELECT * FROM books"
df = pd.read_sql_query(query, connection)

# Print out the data frame to show the full table
print(df)

# Add data stored in a CSV file
csv_data = pd.read_csv('sample_books.csv')

# Add this data to the the existing books db using INSERT
for index, row in csv_data.iterrows():
    cursor.execute('''
        INSERT INTO books (title, price, rating, availability, genre)
        VALUES (?, ?, ?, ?, ?)
    ''', (row['title'], row['price'], row['rating'], row['availability'], row['genre']))

connection.commit()  # Commit after inserting all rows

# Get the new dataframe
df = pd.read_sql_query(query, connection)

# Calculate the average rating
average_rating = df['rating'].mean().round(2)
print(f'Average Rating: {average_rating}')

#  Find the most common rating
most_common_rating = df['rating'].mode()[0]
print(f'Most common rating: {most_common_rating}')
# Display basic statistics
print(df.describe())

# Save the dataframe to a CSV file
df.to_csv('book_data.csv')

# Create Visualizations
# Create a bar plot of the count of books by rating
# Count the number of each rating and then sort the values lowest to highest
rating_counts = df['rating'].value_counts().sort_index()
# 1Format the figure size. This will carry over to the other figures
plt.figure(figsize=(8, 5)) 
# Create a bar chart. The default value for .plot() is a line graph
rating_counts.plot(kind='bar')
# Give the chart a title and label the x and y axis
plt.title('Count of Books by Rating')
plt.xlabel('Rating (Stars)')
plt.ylabel('Count')
# Save the chart. You can also do .show() to show the graph but it will not save the file to your machine.
plt.savefig('bar_chart.png')

# Histogram: Price Distribution
# Create a histogram. Include some additional styling as well
# Use this to indicate a new figure
plt.figure()
plt.hist(df['price'], color='skyblue', edgecolor='black')
plt.title('Price Distribution of Books')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.savefig('histogram.png')


# Scatter Plot: Price vs. Rating
# Create a scatter plot of rating vs. price.
plt.figure()
plt.scatter(df['rating'], df['price'])
plt.title('Price vs. Rating')
plt.xlabel('Rating (Stars)')
plt.ylabel('Price')
plt.savefig('Price_vs_Rating.png')