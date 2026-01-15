from data.database import Database

class RegistratieDetails:
    def __init__(self, db_path):
        self.db = Database(db_path)

def update_status(self, profile_id: int, new_status: str):
    with self.db.connect() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE users SET status = ? WHERE id = ?",
            (new_status, profile_id)
        )
        con.commit()