import sqlite3

class login_account:
    def __init__(self,attribute1,attribute2):
        self.email = attribute1
        self.password = attribute2
        self.correct = "yes"

    def search_user_database_user(self):
        conn = sqlite3.connect('data/app.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ? AND status = 'goedgekeurd'", (self.email, self.password))
        result = c.fetchall()
        if len(result) == 0:
            self.correct = "no" 
            return result
        user_type = result[0][3]
        user_id = result[0][0]
        conn.commit()
        conn.close()
        return user_type, user_id
