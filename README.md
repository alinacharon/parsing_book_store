
# Scraper de Livres

Ce script Python est conçu pour récupérer des informations sur les livres à partir du site Web "Books to Scrape" (https://books.toscrape.com/). Il extrait les détails des livres dans différentes catégories et les enregistre dans des fichiers CSV, ainsi que les images des couvertures dans un dossier dédié.

## Fonctionnalités

- Récupération des informations sur les livres : UPC, titre, prix (TTC et HT), disponibilité, description, catégorie, évaluation, URL de l'image.
- Téléchargement et sauvegarde des images de couverture des livres.
- Enregistrement des détails des livres dans des fichiers CSV organisés par catégorie.

## Utilisation

  1.	Assurez-vous d’avoir Python 3 installé sur votre système.
  2.	Créez un environnement virtuel avec la commande appropriée pour votre système d’exploitation: python -m venv venv pour Windows ou python3 -m venv venv pour Linux/Mac.
  3.	Activez l’environnement virtuel: source venv/bin/activate pour Linux/Mac ou venv\Scripts\activate pour Windows.
  4.	Installez les dépendances en exécutant pip install -r requirements.txt.
  5.	Exécutez le script principal main.py pour démarrer le processus de récupération des informations.

## Comment ça marche

- Le script utilise la bibliothèque `requests` pour effectuer des requêtes HTTP et récupérer le contenu HTML des pages.
- La bibliothèque `BeautifulSoup` est utilisée pour analyser le code HTML et extraire les informations nécessaires.
- Les informations sur les livres sont extraites de différentes pages du site en parcourant les catégories et les pages de résultats.
- Les détails des livres sont ensuite enregistrés dans des fichiers CSV et les images de couverture sont téléchargées dans un dossier dédié.

Pour toute question ou suggestion, veuillez contacter alina.charon@gmail.com
