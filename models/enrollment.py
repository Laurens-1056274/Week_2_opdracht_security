from data.database import Database


class Enrollment:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def count_all(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM enrollments")
            con.commit()
            return cur.fetchone()

    # alle inschrijvingen met naam, organisatie en onderzoek
    def all_with_details(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT
                    e.id,                                           -- 0: inschrijvings-id
                    p.first_name || ' ' || p.last_name AS naam,    -- 1: naam ervaringsdeskundige
                    o.name AS organisatie,                         -- 2: organisatienaam
                    s.title AS onderzoek,                          -- 3: onderzoekstitel
                    e.status                                       -- 4: status
                FROM enrollments e
                JOIN profiles p ON e.profile_id = p.id
                JOIN studies s ON e.study_id = s.id
                JOIN organizations o ON s.organization_id = o.id
            """)
            rows = cur.fetchall()
            return rows

    # status van een inschrijving aanpassen
    def update_status(self, enrollment_id: int, new_status: str):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE enrollments SET status = ? WHERE id = ?",
                (new_status, enrollment_id)
            )
            con.commit()