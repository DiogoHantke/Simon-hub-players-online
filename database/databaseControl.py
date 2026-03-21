import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def createTables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NULL,
                score INTEGER NOT NULL
            )
        """)

def insertScoreDB(score):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO players (score) VALUES(?)",
            (score,)
        )

        conn.commit()

def GetPendingPlayersDB():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM players WHERE username IS NULL")

        rows = cursor.fetchall()

        dataTrated = [row[0] for row in rows]

        return dataTrated

def updateNameDB(idUser, username):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE players
            SET username = ?
            WHERE id = ?
            """,
            (username, idUser)
        )

def searchPlayersDB():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        cursor.execute("""
            SELECT username, score 
            FROM players 
            WHERE username IS NOT NULL
            ORDER BY score DESC
        """)

        rows = cursor.fetchall()

        return [{'username': row['username'], 'score': row['score']} for row in rows]
