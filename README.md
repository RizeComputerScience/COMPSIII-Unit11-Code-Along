# COMPS III: Unit 11 Code Along

## Overview

In the last unit, we scraped data from the [Books to Scrape](https://books.toscrape.com/index.html) website and stored the data in our books database. Now that we have the data, we can use the `pandas` and `matplotlib` libraries to analyze and visualize the data that we scraped and stored last week. 

This week, we’ll be be building functionality to:
- Create a pandas DataFrame from data stored in a database
- Utilize pandas methods to perform statistical calculations
- Create data visualizations using `matplotlib`

By the end of this code along, you will have data that is processed and ready to be analyzed when we work with Python data analysis tools next week!


## Local Terminal
1. In your terminal, install the packages from last week's lab.
```bash
pip install requests bs4 sqlite3 word2number
```
2. In your terminal, install the `pandas` and `matplotlib` libraries.
```bash
pip install pandas matplotlib
```

## VS Code - main.py
3. At the top of the `main.py`, import these modules at the top of the file.
```python
import pandas as pd
import matplotlib.pyplot as plt
```
4. The code from last week has been included to create the scrape the website and save the values in the `books.db` database. Save the data in the database in a dataframe and print out the returned value.
```python
query = "SELECT * FROM books"
df = pd.read_sql_query(query, connection)
print(df)
```

5. We can also add data that is stored in a CSV file into our database. A file called `sample_books.csv` has been added with some additional data we want to add to the file. Call `read_csv()` on `pd` and save the data in a new variable. Iterate through the DataFrame using `.iterrows()` and add the values in the CSV to the `books` database.

```python
csv_data = pd.read_csv('sample_books.csv')

for index, row in csv_data.iterrows():
    cursor.execute('''
        INSERT INTO books (title, price, rating, availability, genre)
        VALUES (?, ?, ?, ?, ?)
    ''', (row['title'], row['price'], row['rating'], row['availability'], row['genre']))
connection.commit() 
```

6. Store the updated database in a DataFrame. Print out the updated value.

```python
df = pd.read_sql_query(query, connection)
print(df)
```

7. Calculate the average rating using the `mean()` method.

```python
average_rating = df['rating'].mean().round(2)
print(f'Average Rating: {average_rating}')
```

8. Find the most common rating using the `mode()` method.

```python
most_common_rating = df['rating'].mode()[0]
print(f'Most common rating: {most_common_rating}')
```

9. Calculating all the statistics by hand is cumbersome. Display the basic statistics for the DataFrame using the `.describe()` method.

```python
print(df.describe())
```

10. Finally, let's export the data that is in the DataFrame to a CSV file that we can easily share with others.
```python
df.to_csv('book_data.csv')
```

11. Using the `matplotlib` library, create a bar plot of the count of books by rating.
    - Count the number of each rating and then sort the values lowest to highest.
    - Format the figure size. This will carry over to the other figures.
    - Create a bar chart. The default value for `.plot()` is a line graph.
    - Give the chart a title and label the x and y axis using the `.title()`, `.xlabel()`, and `.ylabel()` methods.
    - Finally, save the chart. You can also do `.show() `to show the graph but it will not save the file to your machine.

```python
rating_counts = df['rating'].value_counts().sort_index()
plt.figure(figsize=(8, 5)) 
rating_counts.plot(kind='bar')
plt.title('Count of Books by Rating')
plt.xlabel('Rating (Stars)')
plt.ylabel('Count')
plt.savefig('bar_chart.png')
```

12. Create a histogram showing the price distribution in your database.
    - Create a new figure with `.figure()`
    - Call `.hist()` and pass the price value from the DataFrame.
    - Give the graph a title and label the axis using the `.title()`, `.xlabel()`, and `.ylabel()` methods.
    - Save the chart using `.savefig()`.

```python
plt.figure()
plt.hist(df['price'], color='skyblue', edgecolor='black')
plt.title('Price Distribution of Books')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.savefig('histogram.png')
```

13. Finally, create a scatter plot of  vs. price using `.scatter()`.
    - Create a new figure with `.figure()`
    - Call `.scatter()` and pass the price x and y values from the DataFrame.
    - Give the graph a title and label the axis using the `.title()`, `.xlabel()`, and `.ylabel()` methods.
    - Save the chart using `.savefig()`.

```python
plt.figure()
plt.scatter(df['rating'], df['price'])
plt.title('Price vs. Rating')
plt.xlabel('Rating (Stars)')
plt.ylabel('Price')
plt.savefig('Price_vs_Rating.png')
```