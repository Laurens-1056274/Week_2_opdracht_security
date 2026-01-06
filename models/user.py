from data.database import Database

class User:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def count_all(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT() FROM users")
            con.commit()
            return cur.fetchone()

    def get_profile_id(self, user_id: int):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM profiles WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            return row["id"] if row else None

    def profile_by_user_id(self, user_id: int):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                        SELECT first_name, last_name, postcode, phone, intro
                        FROM profiles
                        WHERE user_id = ?
                        """, (user_id,))
            return cur.fetchone()

    def update_profile(self, user_id: int, first_name: str, last_name: str, postcode: str, phone: str, intro: str):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                        UPDATE profiles
                        SET first_name = ?,
                            last_name  = ?,
                            postcode   = ?,
                            phone      = ?,
                            intro      = ?
                        WHERE user_id = ?
                        """, (first_name, last_name, postcode, phone, intro, user_id))
            con.commit()
