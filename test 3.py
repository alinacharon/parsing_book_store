import requests
from bs4 import BeautifulSoup
import csv

# URL страницы с категорией "Путешествия"
url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

# Отправляем GET-запрос на указанный URL
response = requests.get(url)

# Создаем объект Beautiful Soup для анализа HTML-кода
soup = BeautifulSoup(response.content, "html.parser")

# Найдем все книги на странице
books = soup.find_all("h3")

# Создадим CSV-файл для сохранения данных
with open("travel_books.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Price"])

    # Проходим по каждой книге и извлекаем информацию
    for book in books:
        title = book.a["title"]
        price = book.find_next("p", class_="price_color").text

        # Записываем данные в CSV-файл
        writer.writerow([title, price])

print("Данные сохранены в travel_books.csv")
