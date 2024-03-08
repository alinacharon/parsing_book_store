import requests
from bs4 import BeautifulSoup
import csv

def scrape_books_by_category(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Найдем все категории на странице
    categories = soup.find_all("h3")

    for category in categories:
        category_name = category.a.text.strip()
        category_link = "https://books.toscrape.com" + category.a["href"]
        scrape_books_in_category(category_name, category_link)

def scrape_books_in_category(category_name, category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Найдем все книги на странице
    books = soup.find_all("h3")

    # Создадим CSV-файл для сохранения данных
    filename = f"{category_name}_books.csv"
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Price"])

        # Проходим по каждой книге и извлекаем информацию
        for book in books:
            title = book.a["title"]
            price = book.find_next("p", class_="price_color").text

            # Записываем данные в CSV-файл
            writer.writerow([title, price])

    print(f"Данные для категории '{category_name}' сохранены в {filename}")

# Начнем с главной страницы
main_url = "https://books.toscrape.com/index.html"
scrape_books_by_category(main_url)
