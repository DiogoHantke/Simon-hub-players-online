import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def createTables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NULL,
                score INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def insertScoreDB(score):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO players (score) VALUES(?)", (score,))
        conn.commit()


def GetPendingPlayersDB():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM players WHERE username IS NULL OR TRIM(username) = '' ORDER BY id ASC"
        )
        rows = cursor.fetchall()
        return [row[0] for row in rows]


def updateNameDB(idUser, username):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE players SET username = ? WHERE id = ?",
            (username, idUser),
        )
        conn.commit()


def searchPlayersDB():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, username, score, created_at
            FROM players
            WHERE username IS NOT NULL AND TRIM(username) <> ''
            ORDER BY score DESC, created_at ASC, id ASC
            """
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row["id"],
                "username": row["username"],
                "score": row["score"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]
