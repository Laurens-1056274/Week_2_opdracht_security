from data.database import Database

class Registratie:
    def __init__(self, db_path):
        self.db = Database(db_path)

    def get_all_registraties(self):
        con = self.db.connect()
        cursor = con.cursor()
        cursor.execute("SELECT user_id, first_name, last_name FROM profiles")
        return cursor.fetchall()

    def get_profile_details(self, profile_id):
        con = self.db.connect()
        cursor = con.cursor()
        cursor.execute(
            "SELECT * FROM profiles WHERE user_id = ?",
            (profile_id,)
        )
        return cursor.fetchone()




