import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'taskflow.db'


def get_connection():
    """Retorna uma conexão com o banco de dados SQLite."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Cria a tabela de tarefas caso ela ainda não exista."""
    with get_connection() as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL
            )
            '''
        )
        conn.commit()
