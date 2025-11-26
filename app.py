import os
from flask import Flask, render_template, redirect, url_for
from data.database import Database
from models.user import User
from models.organization import Organization
from models.study import Study
from models.enrollment import Enrollment

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

_db = Database(DB_PATH)
users = User(DB_PATH)
organizations = Organization(DB_PATH)
studies = Study(DB_PATH)
enrollments = Enrollment(DB_PATH)
@app.route("/")
def index():
    counts = {
        "experts": users.count_all()[0],
        "organizations": organizations.count_all()[0],
        "studies": studies.count_all()[0],
        "enrollments": enrollments.count_all()[0],
    }
    return render_template("index.html", counts=counts)
@app.route("/beheerder/inschrijvingen")
def beheerder_inschrijvingen():
    #inschrijvingen met details uit de database
    rows = enrollments.all_with_details()

    inschrijvingen = []
    for row in rows:
        inschrijvingen.append({
            "id": row[0],           # inschrijvings-id
            "naam": row[1],         # voor- en achternaam
            "organisatie": row[2],  # organisatienaam
            "onderzoek": row[3],    # onderzoekstitel
            "status": row[4],       # status
        })

    return render_template(
        "pages/beheerder/beheerder_inschrijvingen.html",
        inschrijvingen=inschrijvingen
    )
@app.route("/beheerder/inschrijvingen/<int:inschrijving_id>/goedkeuren")
def inschrijving_goedkeuren(inschrijving_id):
    # status aanpassen naar goedgekeurd
    enrollments.update_status(inschrijving_id, "goedgekeurd")
    return redirect(url_for("beheerder_inschrijvingen"))


@app.route("/beheerder/inschrijvingen/<int:inschrijving_id>/afkeuren")
def inschrijving_afkeuren(inschrijving_id):
    # status aanpassen naar afgekeurd
    enrollments.update_status(inschrijving_id, "afgekeurd")
    return redirect(url_for("beheerder_inschrijvingen"))

if __name__ == "__main__":
    app.run(debug=True)
