import pandas as pd
import os

BOOKS_CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'books.csv')

def load_books_df():
    try:
        df = pd.read_csv(BOOKS_CSV_PATH, index_col='id')
        return df
    except Exception as e:
        raise RuntimeError(f'Erro ao carregar dados dos livros: {e}')
