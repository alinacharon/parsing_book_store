import requests
from bs4 import BeautifulSoup
import csv
import os

BASE_URL = 'https://books.toscrape.com/'

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def save_books_to_csv(books, category_name):
    file_path = f'{category_name}.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Availability'])
        for book in books:
            writer.writerow([book['title'], book['price'], book['availability']])

def get_books_in_category(category_url):
    soup = get_soup(category_url)
    books = []
    for book in soup.select('.product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()
        books.append({'title': title, 'price': price, 'availability': availability})
    return books

def main():
    soup = get_soup(BASE_URL)
    categories = soup.select('.side_categories ul li a')
    for category in categories[1:]:  # skip the first one as it's not a category
        category_name = category.text.strip()
        category_url = BASE_URL + category['href']
        books = get_books_in_category(category_url)
        save_books_to_csv(books, category_name)
        print(f'Сохранено {len(books)} книг в категории {category_name}')

if __name__ == '__main__':
    main()
