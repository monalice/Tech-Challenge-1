import pandas as pd
import os

# Caminho absoluto para garantir localização correta
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BOOKS_CSV_PATH = os.path.join(PROJECT_ROOT, '..', '..', 'data', 'books.csv')

def load_books_df():
    try:
        df = pd.read_csv(BOOKS_CSV_PATH, index_col='id')
        return df
    except Exception as e:
        raise RuntimeError(f'Erro ao carregar dados dos livros: {e}')
