import sqlite3
from werkzeug.security import check_password_hash

class login_account:
    def __init__(self,attribute1,attribute2):
        self.email = attribute1
        self.password = attribute2
        self.correct = "yes"

    def search_user_database_user(self):
        conn = sqlite3.connect('data/app.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND status = 'goedgekeurd'", (self.email,))
        result = c.fetchall()
        if len(result) == 0 or not check_password_hash(result[0][2], self.password):
            self.correct = "no" 
            return result
        user_type = result[0][3]
        user_id = result[0][0]
        conn.commit()
        conn.close()
        return user_type, user_id
