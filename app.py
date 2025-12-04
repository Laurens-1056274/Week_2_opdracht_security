import os
from flask import Flask, render_template,request,redirect,url_for
from data.database import Database
from models.user import User
from models.organization import Organization
from models.study import Study
from models.enrollment import Enrollment
from add_new_organisationaccount import submit_organisation_account


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
    return render_template("pages/index.html", counts=counts)
@app.route("/beheerder/inschrijvingen")
def beheerder_inschrijvingen():
    # echte inschrijvingen met details uit de database
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
        "beheerder_inschrijvingen.html",
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

@app.route("/ervaringsdeskunidge_dashboard")
def ervaringsdeskunidge_dashboard():
    return render_template("pages/ervaringsDeskundigeDashboard.html", 
                           page_title="dashboard",
                           description="Ervarings Deskundige Dashboard")

@app.route("/register")
def register_page():
    return render_template("pages/login/register.html", 
                           page_title="Register",
                           description="Ervarings Deskundige Register page")

@app.route("/login")
def login_page():
    return render_template("pages/login/login.html", 
                           page_title="Login",
                           description="Ervarings Deskundige Login page")


@app.route("/OrganisatieAccount")
def OrganisatieAccount():
    return render_template("pages/beheerder/maak_organisatieaccount.html", 
                           page_title="OrganisatieAccount", 
                           description="Pagina om een organisatieaccount aan te maken. Vul het formulier in om een organisatie toe te voegen.")

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        return redirect("/")
    data = request.form
    submit_organisation_account(
    data["name"],
    data["type"],
    data["website"],
    data["description"],
    data["contact_person"],
    data["email"],
    data["phone"],
    data["details"]
    ).add_to_database()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
