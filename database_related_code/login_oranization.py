import sqlite3



class login_account_organization:
    def __init__(self,attribute1,attribute2):
        self.email = attribute1
        self.phone = attribute2
        self.correct = "yes"

    def search_user_database(self):
        conn = sqlite3.connect('data/app.db')
        c = conn.cursor()
        c.execute("SELECT * FROM organizations WHERE email = ? AND phone = ?", (self.email, self.phone))
        result = c.fetchall()
        if len(result) == 0:
            self.correct = "no" 
        else:
            organization_name = result[0][1]
            organization_id = result[0][0]
        conn.commit()
        conn.close()
        return organization_name, organization_id
