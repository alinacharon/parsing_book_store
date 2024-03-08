import requests
from bs4 import BeautifulSoup
import csv
import os

BASE_URL = 'https://books.toscrape.com/'

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def save_books_to_csv(books, category_name,folder_name="Books_csv"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, f'{category_name}.csv')
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['UPC', 'Title', 'Price (incl. tax)', 'Price (excl. tax)', 'Availability', 'Description', 'Category', 'Rating', 'Image URL'])
        for book in books:
            writer.writerow([book['upc'], book['title'], book['price_incl_tax'], book['price_excl_tax'], book['availability'], book['description'], book['category'], book['rating'], book['image_url']])

def get_book_details(book_url):
    
    book_url = book_url.replace('index.html', '').replace('catalogue/', '')
    full_url = f'{BASE_URL}catalogue/{book_url}index.html'
    soup = get_soup(full_url)


    product_info = soup.find('table', class_='table table-striped').find_all('td')
    description = soup.find('meta', attrs={'name': 'description'})['content'].strip()
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    rating = soup.select_one('p.star-rating')['class'][1]
    image_url = BASE_URL + soup.find('img')['src']
    return {
        'upc': product_info[0].text,
        'title': soup.find('div', class_='product_main').h1.text,
        'price_incl_tax': product_info[3].text.replace('Â',''),
        'price_excl_tax': product_info[2].text.replace('Â',''),
        'availability': product_info[5].text.split('(')[1].split(' ')[0],
        'description': description,
        'category': category,
        'rating': rating,
        'image_url': image_url
    }

def get_books_in_category(category_url):
    books = []
    page_number = 1
    while True:
        page_url = f'{category_url}page-{page_number}.html'
        response = requests.get(page_url)
        if response.status_code == 404:
            print("Processing page:", page_url)
            break
        soup = get_soup(page_url)
        new_books = soup.select('.product_pod')
        if not new_books:
            break
        for book in new_books:
            book_url = BASE_URL + book.h3.a['href']
            books.append(get_book_details(book_url))
        page_number += 1
    return books

def main():
    folder_name = 'Books_csv'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    soup = get_soup(BASE_URL)
    categories = soup.select('.side_categories ul li a')
    for category in categories[1:]:  # skip the first one as it's not a category
        category_name = category.text.strip()
        category_url = BASE_URL + category['href']
        books = get_books_in_category(category_url)
        save_books_to_csv(books, category_name, folder_name)
        print(f'Сохранено {len(books)} книг в категории {category_name} в папку {folder_name}')

if __name__ == '__main__':
    main()
