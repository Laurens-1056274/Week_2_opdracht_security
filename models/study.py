import sqlite3
from data.database import Database


class Study:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def count_all(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM studies")
            return cur.fetchone()
        
    def update_status(self, study_id: int, new_status: str):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE studies SET status = ? WHERE id = ?",
                (new_status, study_id)
            )
            con.commit()

    def all_with_details(self):
        with self.db.connect() as con:
            con.row_factory = sqlite3.Row  # <-- this makes rows dictionary-like
            cur = con.cursor()
            cur.execute("""
                SELECT
                    s.id,
                    s.title,
                    s.organization_id,
                    s.status,
                    o.name AS organisatie
                FROM studies s
                JOIN organizations o ON s.organization_id = o.id
                ORDER BY s.start_date DESC
            """)
            return cur.fetchall()  # now each row behaves like a dict