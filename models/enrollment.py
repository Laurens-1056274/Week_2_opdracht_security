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


    def all_with_details(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT
                    e.id,                                           
                    p.first_name || ' ' || p.last_name AS naam,    
                    o.name AS organisatie,                       
                    s.title AS onderzoek,                          
                    e.status                                      
                FROM enrollments e
                JOIN profiles p ON e.profile_id = p.id
                JOIN studies s ON e.study_id = s.id
                JOIN organizations o ON s.organization_id = o.id
            """)
            rows = cur.fetchall()
            return rows

    def update_status(self, enrollment_id: int, new_status: str):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE enrollments SET status = ? WHERE id = ?",
                (new_status, enrollment_id)
            )
            con.commit()

    def all_for_profile(self, profile_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT e.id, s.title, e.status
                FROM enrollments e
                JOIN studies s ON e.study_id = s.id
                WHERE e.profile_id = ?
            """, (profile_id,))
            return cur.fetchall()

    def create(self, profile_id, study_id):
        conn = self.db.connect()
        conn.execute("""
        INSERT INTO enrollments (profile_id, study_id, status)
        VALUES (?, ?, 'in afwachting')
        """, (profile_id, study_id))
        conn.commit()
        conn.close()
    def approved_for_org(self, org_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                        SELECT e.id,
                               p.first_name || ' ' || p.last_name,
                               s.title,
                               e.created_at
                        FROM enrollments e
                                 JOIN profiles p ON p.id = e.profile_id
                                 JOIN studies s ON s.id = e.study_id
                        WHERE s.organization_id = ?
                          AND e.status = 'goedgekeurd'
                        """, (org_id,))
            return cur.fetchall()

