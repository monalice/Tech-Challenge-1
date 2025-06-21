import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
import re

logger = logging.getLogger("scraper")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

BASE_URL = 'http://books.toscrape.com/'

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def fetch_page(url: str) -> Optional[BeautifulSoup]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        logger.error(f"Erro ao requisitar {url}: {e}")
        return None

def parse_book(article, category: str) -> Optional[Dict]:
    try:
        title = article.h3.a["title"].strip()
        price_text = article.find(class_="price_color").text
        price_clean = re.sub(r'[^\d.,]', '', price_text)
        price_clean = price_clean.replace(',', '.')
        price = float(price_clean)
        rating = RATING_MAP.get(article.p["class"][1], 0)
        availability = article.find(class_="availability").text.strip()
        image_url = BASE_URL + article.find("img")["src"].replace("../", "")
        return {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "category": category,
            "image_url": image_url
        }
    except Exception as e:
        logger.error(f"Erro ao parsear livro: {e}")
        return None

def get_category_links(main_soup: BeautifulSoup) -> List[str]:
    links = []
    for a in main_soup.select(".side_categories ul li ul li a"):
        href = a.get("href")
        if isinstance(href, list):
            href = href[0] if href else None
        if href:
            url = BASE_URL.rstrip("/") + "/" + str(href).lstrip("/")
            links.append(url)
    return links
