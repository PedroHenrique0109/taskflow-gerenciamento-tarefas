import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'taskflow.db'


def get_db_path():
    """Retorna o caminho do banco SQLite configurado ou o banco principal."""
    database_path = os.getenv('TASKFLOW_DB_PATH')
    return Path(database_path) if database_path else DB_PATH


def get_connection():
    """Retorna uma conexão com o banco de dados SQLite."""
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Cria a tabela de tarefas com prioridade ou atualiza a tabela existente."""
    with get_connection() as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'Média'
            )
            '''
        )

        cursor = conn.execute("PRAGMA table_info(tasks)")
        columns = [row['name'] for row in cursor.fetchall()]
        if 'priority' not in columns:
            conn.execute("ALTER TABLE tasks ADD COLUMN priority TEXT NOT NULL DEFAULT 'Média'")
        conn.commit()
