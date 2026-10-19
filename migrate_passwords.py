"""Migrate previously stored plain text user passwords to Werkzeug password hashes.
Run once after taking a database backup. Never put the database in Git.
"""
import os
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "app.db")

if __name__ == "__main__":
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute("SELECT id, password FROM users").fetchall()
        for user_id, password in rows:
            if password and not password.startswith(("scrypt:", "pbkdf2:")):
                connection.execute("UPDATE users SET password = ? WHERE id = ?",
                                   (generate_password_hash(password), user_id))
        connection.commit()
    print("Migratie voltooid. Organisaties moeten mogelijk nieuwe inloggegevens krijgen.")
