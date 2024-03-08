import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Отправляем запрос на страницу
url = "https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html"
response = requests.get(url)
page_content = response.content

# Создаем объект BeautifulSoup для парсинга HTML
soup = BeautifulSoup(page_content, "html.parser")

# URL страницы продукта
product_page_url = url

# Находим все книги на странице
books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

# Создаем список для хранения данных о книгах
data = []

for book in books:
    # Пытаемся найти универсальный код продукта (UPC)
    try: 
        universal_product_code = soup.find("th", string="UPC").find_next_sibling("td").text
    except:    
        universal_product_code = "-"

    # Находим название книги
    title = book.h3.a["title"]

    # Находим цену с учетом налога
    price_including_tax = book.find("p", class_="price_color").text.strip()

    # Пытаемся найти цену без учета налога
    try: 
        price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").text
    except: 
        price_excluding_tax = "-"

    # Находим количество доступных книг
    number_available = book.find("p", class_="instock availability").text.strip()

    # Пытаемся найти описание продукта
    try: 
        product_description = book.find("p", class_="").text.strip()
    except: 
        product_description = "-"

    # Находим категорию книги
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()

    # Находим рейтинг книги
    review_rating = book.p["class"][1]

    # Находим URL страницы продукта
    relative_url = book.find("h3").find("a")["href"]
    absolute_url = urljoin(url, relative_url)  # Объединяем базовый URL и относительный URL книги

    # Добавляем данные в список
    data.append([
        product_page_url,
        universal_product_code,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        review_rating,
        absolute_url  # Используем абсолютный URL книги
    ])

# Записываем данные в CSV файл
with open("data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "product_page_url",
        "universal_product_code (upc)",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "product_url"
    ])
    writer.writerows(data)

print("The csv file has been successfully created.")

