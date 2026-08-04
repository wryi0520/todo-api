from typing import Optional

import psycopg

from app.schemas import TodoCreate, TodoUpdate


def create_todo(conn: psycopg.Connection, todo: TodoCreate) -> Optional[dict]:
    row = conn.execute(
        """
        INSERT INTO todos (title, description, completed, due_date, priority)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (todo.title, todo.description, todo.completed, todo.due_date, todo.priority),
    ).fetchone()
    conn.commit()
    return get_todo(conn, row["id"])


def get_todo(conn: psycopg.Connection, todo_id: int) -> Optional[dict]:
    row = conn.execute("SELECT * FROM todos WHERE id = %s", (todo_id,)).fetchone()
    return dict(row) if row else None


def list_todos(conn: psycopg.Connection) -> list[dict]:
    rows = conn.execute("SELECT * FROM todos ORDER BY id").fetchall()
    return [dict(row) for row in rows]


def update_todo(conn: psycopg.Connection, todo_id: int, todo: TodoUpdate) -> Optional[dict]:
    fields = todo.model_dump(exclude_unset=True)
    if not fields:
        return get_todo(conn, todo_id)

    assignments = ", ".join(f"{key} = %s" for key in fields)
    values = list(fields.values()) + [todo_id]
    conn.execute(
        f"UPDATE todos SET {assignments}, updated_at = now() WHERE id = %s",
        values,
    )
    conn.commit()
    return get_todo(conn, todo_id)


def delete_todo(conn: psycopg.Connection, todo_id: int) -> bool:
    cursor = conn.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()
    return cursor.rowcount > 0
