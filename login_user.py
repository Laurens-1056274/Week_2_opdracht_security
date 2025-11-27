import sqlite3



class login_account:
    def __init__(self,attribute1,attribute2):
        self.email = attribute1
        self.password = attribute2

    def search_user_database(self):
        conn = sqlite3.connect('data/app.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (self.email, self.password))
        result = c.fetchall()
        if len(result) == 0:
            print('uh oh, no existing account silly!')
        
        else:
            print(result[0])
        conn.commit()
        conn.close()
