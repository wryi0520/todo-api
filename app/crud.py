import sqlite3
from typing import Optional

from app.schemas import TodoCreate, TodoUpdate


def create_todo(conn: sqlite3.Connection, todo: TodoCreate) -> Optional[dict]:
    cursor = conn.execute(
        """
        INSERT INTO todos (title, description, completed, due_date, priority)
        VALUES (?, ?, ?, ?, ?)
        """,
        (todo.title, todo.description, int(todo.completed), todo.due_date, todo.priority),
    )
    conn.commit()
    return get_todo(conn, cursor.lastrowid)


def get_todo(conn: sqlite3.Connection, todo_id: int) -> Optional[dict]:
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    return dict(row) if row else None


def list_todos(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("SELECT * FROM todos ORDER BY id").fetchall()
    return [dict(row) for row in rows]


def update_todo(conn: sqlite3.Connection, todo_id: int, todo: TodoUpdate) -> Optional[dict]:
    fields = todo.model_dump(exclude_unset=True)
    if not fields:
        return get_todo(conn, todo_id)

    if "completed" in fields:
        fields["completed"] = int(fields["completed"])

    assignments = ", ".join(f"{key} = ?" for key in fields)
    values = list(fields.values()) + [todo_id]
    conn.execute(
        f"UPDATE todos SET {assignments}, updated_at = STRFTIME('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
        values,
    )
    conn.commit()
    return get_todo(conn, todo_id)


def delete_todo(conn: sqlite3.Connection, todo_id: int) -> bool:
    cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    return cursor.rowcount > 0
