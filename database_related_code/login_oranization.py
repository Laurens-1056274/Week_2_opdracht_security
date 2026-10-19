import sqlite3
from werkzeug.security import check_password_hash



class login_account_organization:
    def __init__(self,attribute1,attribute2):
        self.email = attribute1
        self.password = attribute2
        self.correct = "yes"

    def search_user_database_organization(self):
        conn = sqlite3.connect('data/app.db')
        c = conn.cursor()
        c.execute("""SELECT o.id, o.name, u.password FROM organizations o
                     JOIN users u ON u.organization_id = o.id
                     WHERE o.email = ? AND u.email = ? AND u.role = 'organization'
                       AND u.status = 'goedgekeurd'""", (self.email, self.email))
        result = c.fetchall()
        if len(result) == 0 or not check_password_hash(result[0][2], self.password):
            self.correct = "no" 
            return result
        else:
            organization_name = result[0][1]
            organization_id = result[0][0]
        conn.commit()
        conn.close()
        return organization_name, organization_id
