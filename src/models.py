from dataclasses import dataclass
from src.database import get_connection

STATUS_OPTIONS = ['Pendente', 'Em andamento', 'Concluída']


@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str


def row_to_task(row):
    return Task(
        id=row['id'],
        title=row['title'],
        description=row['description'],
        status=row['status'],
    )


def get_all_tasks():
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM tasks ORDER BY id DESC')
        return [row_to_task(row) for row in cursor.fetchall()]


def get_task(task_id):
    with get_connection() as conn:
        row = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        return row_to_task(row) if row else None


def create_task(title, description):
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)',
            (title, description, STATUS_OPTIONS[0]),
        )
        conn.commit()


def update_task(task_id, title, description, status):
    with get_connection() as conn:
        conn.execute(
            'UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?',
            (title, description, status, task_id),
        )
        conn.commit()


def delete_task(task_id):
    with get_connection() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()


def change_status(task_id, status):
    with get_connection() as conn:
        conn.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
        conn.commit()
