import csv
import logging
from scraper_utils import fetch_page, parse_book, get_category_links
from typing import List, Dict
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scraper")

BASE_URL = "http://books.toscrape.com/"
CSV_PATH = "data/books.csv"


def get_category_name(soup: BeautifulSoup) -> str:
    breadcrumb = soup.select(".breadcrumb li li")
    if len(breadcrumb) >= 2:
        return breadcrumb[-1].text.strip()
    h1 = soup.select_one(".page-header h1")
    if h1:
        return h1.text.strip()
    return ""


def scrape_all_books() -> List[Dict]:
    logger.info("Iniciando scraping de todas as categorias...")
    main_soup = fetch_page(BASE_URL)
    if not main_soup:
        logger.error("Não foi possível carregar a página principal.")
        return []
    categories = get_category_links(main_soup)
    all_books = []
    book_id = 1
    for cat_url in categories:
        page_url = cat_url
        category = None
        while True:
            soup = fetch_page(page_url)
            if not soup:
                logger.error(f"Falha ao carregar página: {page_url}")
                break
            if category is None:
                category = get_category_name(soup)
            articles = soup.select("article.product_pod")
            for article in articles:
                book = parse_book(article, category)
                if book:
                    book["id"] = book_id
                    all_books.append(book)
                    book_id += 1
            next_btn = soup.select_one("li.next > a")
            if next_btn:
                next_href = next_btn.get("href")
                if not next_href:
                    break
                if isinstance(page_url, list):
                    page_url = page_url[0]
                if "/" in page_url:
                    page_url = "/".join(str(page_url).split("/")[:-1]) + "/" + str(next_href)
                else:
                    page_url = str(next_href)
            else:
                break
    logger.info(f"Total de livros extraídos: {len(all_books)}")
    return all_books


def save_books_csv(books: List[Dict], path: str = CSV_PATH):
    if not books:
        logger.warning("Nenhum livro para salvar.")
        return
    fieldnames = ["id", "title", "price", "rating", "availability", "category", "image_url"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book)
    logger.info(f"Dados salvos em {path}")


if __name__ == "__main__":
    books = scrape_all_books()
    save_books_csv(books)
