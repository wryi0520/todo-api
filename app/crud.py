from typing import Optional

import psycopg

from app.schemas import TodoCreate, TodoUpdate, UserCreate
from app.security import hash_password


def create_user(conn: psycopg.Connection, user: UserCreate) -> Optional[dict]:
    row = conn.execute(
        """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (user.username, user.email, hash_password(user.password)),
    ).fetchone()
    conn.commit()
    return get_user(conn, row["id"])


def get_user(conn: psycopg.Connection, user_id: int) -> Optional[dict]:
    row = conn.execute("SELECT * FROM users WHERE id = %s", (user_id,)).fetchone()
    return dict(row) if row else None


def get_user_by_username(conn: psycopg.Connection, username: str) -> Optional[dict]:
    row = conn.execute("SELECT * FROM users WHERE username = %s", (username,)).fetchone()
    return dict(row) if row else None


def get_user_by_email(conn: psycopg.Connection, email: str) -> Optional[dict]:
    row = conn.execute("SELECT * FROM users WHERE email = %s", (email,)).fetchone()
    return dict(row) if row else None


def create_todo(conn: psycopg.Connection, user_id: int, todo: TodoCreate) -> Optional[dict]:
    row = conn.execute(
        """
        INSERT INTO todos (user_id, title, description, completed, due_date, priority)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (user_id, todo.title, todo.description, todo.completed, todo.due_date, todo.priority),
    ).fetchone()
    conn.commit()
    return get_todo(conn, user_id, row["id"])


def get_todo(conn: psycopg.Connection, user_id: int, todo_id: int) -> Optional[dict]:
    row = conn.execute(
        "SELECT * FROM todos WHERE id = %s AND user_id = %s", (todo_id, user_id)
    ).fetchone()
    return dict(row) if row else None


def list_todos(conn: psycopg.Connection, user_id: int) -> list[dict]:
    rows = conn.execute(
        "SELECT * FROM todos WHERE user_id = %s ORDER BY id", (user_id,)
    ).fetchall()
    return [dict(row) for row in rows]


def update_todo(conn: psycopg.Connection, user_id: int, todo_id: int, todo: TodoUpdate) -> Optional[dict]:
    fields = todo.model_dump(exclude_unset=True)
    if not fields:
        return get_todo(conn, user_id, todo_id)

    assignments = ", ".join(f"{key} = %s" for key in fields)
    values = list(fields.values()) + [todo_id, user_id]
    conn.execute(
        f"UPDATE todos SET {assignments}, updated_at = now() WHERE id = %s AND user_id = %s",
        values,
    )
    conn.commit()
    return get_todo(conn, user_id, todo_id)


def delete_todo(conn: psycopg.Connection, user_id: int, todo_id: int) -> bool:
    cursor = conn.execute(
        "DELETE FROM todos WHERE id = %s AND user_id = %s", (todo_id, user_id)
    )
    conn.commit()
    return cursor.rowcount > 0
