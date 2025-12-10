import sqlite3


class submit_organisation_account:
    def __init__(self,attribute1,attribute2,attribute3,attribute4,attribute5,attribute6,attribute7,attribute8):
        self.name = attribute1
        self.type = attribute2
        self.website = attribute3
        self.description = attribute4
        self.contact_person = attribute5
        self.email = attribute6
        self.phone = attribute7
        self.details = attribute8
        if self.details == "":
            self.details = None

    def add_to_database(self):
        conn = sqlite3.connect('data/app.db')
        c = conn.cursor()
        c.execute("INSERT INTO organizations (name,type,website,description,contact_person,email,phone,details)" \
        "VALUES (?,?,?,?,?,?,?,?)",(self.name,self.type,self.website,self.description,self.contact_person,self.email,self.phone,self.details))
        conn.commit()
        conn.close()
