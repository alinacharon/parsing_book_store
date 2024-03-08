import requests
from bs4 import BeautifulSoup
import csv

# Функция для парсинга страницы и извлечения категорий книг
def parse_categories(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        categories = soup.find('ul', class_='nav-list').find_all('a')
        return [category.text.strip() for category in categories]
    else:
        print("Ошибка при загрузке страницы")
        return []

# URL страницы с категориями книг
url = "https://books.toscrape.com/catalogue/category/books_1/index.html"

# Извлекаем категории книг
categories = parse_categories(url)

# Записываем категории книг в CSV файл
with open("book_categories.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Категория книг"])
    writer.writerows([[category] for category in categories])

print("Категории книг успешно записаны в файл book_categories.csv")