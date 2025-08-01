import requests
from bs4 import BeautifulSoup
import pandas as pd

# creating lists for the dataframe
titles_col = []
prices_col = []
availability_col = []
rating_col = []

#preparing a map to convert the book-rating-strings to numbers
rating_map = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

# iterating through multiple pages on website
for i in range(1,51):

    # get html data and create parser
    url = requests.get(f"https://books.toscrape.com/catalogue/category/books_1/page-{i}.html")
    soup = BeautifulSoup(url.content, "lxml")

    # obtaining the specific part of the code I need
    books = soup.find_all('article', class_='product_pod')

    # iterating through the required tags and adding data to the lists
    for book in books:
        title = book.h3.a['title'].strip()
        price = book.find('p', class_ = 'price_color').text.strip()
        availability = book.find('p', class_ = 'instock availability').text.strip()
        rating = book.find('p')['class'][1]

        titles_col.append(title)
        prices_col.append(price)
        availability_col.append(availability)
        rating_col.append(rating)

# creating the dataframe
pd.set_option('display.max_colwidth', None)
df = pd.DataFrame(data = {'Book_title': titles_col, 'Book_prices': prices_col, 'Availability': availability_col, 'Rating': rating_col})

# cleaning the dataframe
df['Book_prices'] = df['Book_prices'].str.replace('£', '', regex=False).astype(float)
df['Rating'] = df['Rating'].map(rating_map)

#overview of the dataframe
df.head()

# exporting the dataframa as a csv file
df.to_csv('Book_scraping.csv')