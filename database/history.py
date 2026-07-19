import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "elearning.db"


def save_history(user_id, course_title):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute(
        """
        INSERT INTO recommendation_history
        (user_id, course_title, recommended_at)
        VALUES (?, ?, ?)
        """,
        (user_id, course_title, current_time)
    )

    conn.commit()
    conn.close()


def get_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT course_title, recommended_at
        FROM recommendation_history
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows