import requests
from bs4 import BeautifulSoup
import os

def download_image(image_url, image_folder):
    """Télécharge et enregistre l'image à partir de l'URL spécifiée."""
    filename = image_url.split('/')[-1]
    filepath = os.path.join(image_folder, filename)
    with open(filepath, 'wb') as file:
        response = requests.get(image_url)
        file.write(response.content)
    print(f"L'image a été téléchargée et enregistrée sous {filepath}")

def main():
    """Fonction principale pour télécharger une image de livre."""
    image_folder = 'images_de_livres_telecharges'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    
    product_url = input("Veuillez entrer le lien du produit sur le site https://books.toscrape.com/index.html : ")
    response = requests.get(product_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tag = soup.find('div', class_='item active').find('img')
        if image_tag:
            image_url = 'https://books.toscrape.com/' + image_tag['src'].replace('../', '')
            download_image(image_url, image_folder)
        else:
            print("Lien d'image introuvable.")
    else:
        print("Impossible d'accéder à la page du produit.")

if __name__ == '__main__':
    main()