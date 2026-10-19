import sqlite3
from werkzeug.security import generate_password_hash


class submit_organisation_account:
    def __init__(self,attribute1,attribute2,attribute3,attribute4,attribute5,attribute6,attribute7,attribute8,password):
        self.name = attribute1
        self.type = attribute2
        self.website = attribute3
        self.description = attribute4
        self.contact_person = attribute5
        self.email = attribute6
        self.phone = attribute7
        self.details = attribute8
        self.password = password
        if self.details == "":
            self.details = None
        self.correct = "yes"

    def add_to_database(self):
        conn = sqlite3.connect('data/app.db')
        c = conn.cursor()


        c.execute("SELECT * FROM organizations WHERE email = ? AND phone = ?",(self.email,self.phone))
        result = c.fetchall()
        if len(result) > 0:
            self.correct = "no"
            return self.correct

        c.execute("INSERT INTO organizations (name,type,website,description,contact_person,email,phone,details)" \
        "VALUES (?,?,?,?,?,?,?,?)",(self.name,self.type,self.website,self.description,self.contact_person,self.email,self.phone,self.details))
        organization_id = c.lastrowid
        c.execute("INSERT INTO users (email, password, role, status, organization_id) VALUES (?, ?, ?, ?, ?)",
                  (self.email, generate_password_hash(self.password), "organization", "goedgekeurd", organization_id))
        conn.commit()
        conn.close()
        return
