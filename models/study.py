from data.database import Database


class Study:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def count_all(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT() FROM studies")
            con.commit()
            return cur.fetchone()
        
    def update_status(self, study_id: int, new_status: str):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE studies SET status = ? WHERE id = ?",
                (new_status, study_id)
            )
            con.commit()