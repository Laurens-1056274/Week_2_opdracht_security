import sqlite3

class submit_organization_onderzoek:
    def __init__(
        self,
        organization_id,
        title,
        description,
        start_date,
        end_date,
        study_type,
        location,
        has_reward,
        reward,
        age_min,
        age_max,
        status="nieuw",
        available=1
    ):
        self.organization_id = organization_id
        self.title = title
        self.status = status
        self.available = available
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.study_type = study_type
        self.location = location
        self.has_reward = has_reward
        self.reward = reward
        self.age_min = age_min
        self.age_max = age_max

    def add_to_database(self):
        with sqlite3.connect("data/app.db", timeout=10) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO studies (
                    organization_id,
                    title,
                    available,
                    description,
                    start_date,
                    end_date,
                    study_type,
                    location,
                    has_reward,
                    reward,
                    age_min,
                    age_max
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.organization_id,
                self.title,
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

