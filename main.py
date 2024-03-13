import requests
from bs4 import BeautifulSoup
import csv
import os

BASE_URL = 'https://books.toscrape.com/'

def get_soup(url):
    #Récupère le code source HTML de l'URL spécifiée.
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def save_books_to_csv(books, category_name, folder_name="Books_csv"):
    #Enregistre les informations des livres dans un fichier CSV.
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, f'{category_name}.csv')
    with open(file_path, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['UPC', 'Title', 'Price (incl. tax)', 'Price (excl. tax)', 'Availability', 'Description', 'Category', 'Rating', 'Image URL'])
        for book in books:
            writer.writerow([book['upc'], book['title'], book['price_incl_tax'], book['price_excl_tax'], book['availability'], book['description'], book['category'], book['rating'], book['image_url']])

def download_image(image_url, folder_name, filename):
    #Télécharge et enregistre l'image avec le nom spécifié.
    filepath = os.path.join(folder_name, filename)
    with open(filepath, 'wb') as file:
        response = requests.get(image_url)
        file.write(response.content)

def get_book_details(book_url, image_folder, book_title):
    #Récupère les détails d'un livre.
    book_url = book_url.replace('index.html', '').replace('catalogue/', '')
    full_url = f'{BASE_URL}catalogue/{book_url}index.html'
    soup = get_soup(full_url)

    book_title = soup.find('div', class_='product_main').h1.text
    product_info = soup.find('table', class_='table table-striped').find_all('td')
    description = soup.find('meta', attrs={'name': 'description'})['content'].strip()
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    rating = soup.select_one('p.star-rating')['class'][1]
    image_url = BASE_URL + soup.find('img')['src']
    upc = soup.find("th", string="UPC").find_next_sibling("td").text
    filename = download_image(image_url, image_folder, f'{book_title}.jpg'.replace ('/',' ' ))
    return {
        'upc': upc,
        'title': book_title,
        'price_incl_tax': product_info[3].text.replace('Â',''),
        'price_excl_tax': product_info[2].text.replace('Â',''),
        'availability': product_info[5].text.split('(')[1].split(' ')[0],
        'description': description,
        'category': category,
        'rating': rating,
        'image_url': image_url,
        'image_filename': filename
    }


def get_books_in_category(category_url, image_folder):
    #Récupère tous les livres dans une catégorie.
    books = []
    page_number = 1
    while True:
        page_url = f'{category_url.replace("index.html","")}page-{page_number}.html' if page_number > 1 else category_url
        response = requests.get(page_url)
        
        if response.status_code == 404:
            break
        
        soup = get_soup(page_url)
        new_books = soup.select('.product_pod')
        if not new_books:
            break
        
        for book in new_books:
            book_url = BASE_URL + book.h3.a['href']
            title = book.h3.a['title']
            books.append(get_book_details(book_url, image_folder, title))
        
        page_number += 1
    
    return books

def main():
   #Fonction principale pour récupérer les informations des livres.
    folder_name = 'Books_csv'
    image_folder = 'Books_images'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    
    soup = get_soup(BASE_URL)
    categories = soup.select('.side_categories ul li a')
    
    for category in categories[1:]: 
        category_name = category.text.strip()
        category_url = BASE_URL + category['href']
        print('Traitement de la catégorie:', category_name, 'est en cours')  # Message de processus 
        books = get_books_in_category(category_url, image_folder)
        save_books_to_csv(books, category_name, folder_name)
        print(f'{len(books)} livres enregistrés dans la catégorie {category_name} dans le dossier {folder_name}')

if __name__ == '__main__':
    main()
