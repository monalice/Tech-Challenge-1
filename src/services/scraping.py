from script.scraper_books import scrape_all_books, save_books_db
import logging

def trigger_scraping():
    books = scrape_all_books()
    if books:
        save_books_db(books)
        logging.getLogger("uvicorn.error").info(f"Scraping executado manualmente. Livros salvos: {len(books)}")
        return {"detail": "Scraping executado com sucesso", "books_scraped": len(books)}
    return {"detail": "Nenhum livro novo encontrado"}