import sqlite3


class submit_organization_onderzoek:
    def __init__(self,attribute1,attribute2,attribute3,attribute4,attribute5,attribute6,attribute7,attribute8,attribute9,attribute10,attribute11,attribute12,attribute13,attribute14):
        self.id = attribute1
        self.organization_id = attribute2
        self.title = attribute3
        self.status = attribute4
        self.available = attribute5
        self.description = attribute6
        self.start_date = attribute7
        self.end_date = attribute8
        self.study_type = attribute9
        self.location = attribute10
        self.has_reward = attribute11
        self.reward = attribute12
        self.age_min = attribute13
        self.age_max = attribute14

def add_to_database(self):
    conn = sqlite3.connect('data/app.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO studies 
        (organization_id, title, type, status, available, description, start_date, end_date, study_type, location, has_reward, reward, age_min, age_max)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        self.organization_id,  
        self.title,
        self.type,
        self.status,
        self.available,
        self.description,
        self.start_date,
        self.end_date,
        self.study_type,
        self.location,
        self.has_reward,
        self.reward,
        self.age_min,
        self.age_max
    ))
    conn.commit()
    conn.close()

