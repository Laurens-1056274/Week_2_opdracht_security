import os
from flask import Flask, render_template,request,redirect,session,url_for
from data.database import Database
from models.user import User
from models.organization import Organization
from models.study import Study
from models.enrollment import Enrollment
from database_related_code.add_new_organisationaccount import submit_organisation_account
from database_related_code.login_oranization import login_account_organization
from database_related_code.login_user import login_account

app = Flask(__name__)
app.secret_key = "hello"
startup_code = True
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

_db = Database(DB_PATH)
users = User(DB_PATH)
organizations = Organization(DB_PATH)
studies = Study(DB_PATH)
enrollments = Enrollment(DB_PATH)
user_role_admin = False
user_role_organization = False
user_role_expert = False

@app.route("/")
def index():
    global startup_code
    if startup_code == True:
        session.clear()
        startup_code = False
    try:
        if session["user_type"] == "admin" or session["user_type"] == "organization" or session["user_type"] == "expert":
            pass
        else:
            session["user_type"] = "not defined"
            session["type_login"] = "-"
    except:
        session["user_type"] = "not defined"
        session["type_login"] = "-"
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

@app.route("/ervaringsdeskundige_registratie/int:id>")
def ervaringsdeskundige_registratie():
    return render_template("templates/pages/beheerder/registratie_details.html",
                                    page_title="",
                                    description="pagina voor het inzien van de registraties van de ervaringsdeskundigen")

@app.route("/ervaringsdeskunidge_dashboard")
def ervaringsdeskunidge_dashboard():
    return render_template("pages/ervaringsDeskundigeDashboard.html", 
                           page_title="dashboard",
                           description="Ervarings Deskundige Dashboard")

@app.route("/login_check_user", methods=["GET", "POST"])
def check_login_user():
    # user type admin = beheerder, user type organization = organisatie, user type expert = ervaringsdeskundige
    if request.method == "GET":
        return redirect("/")
    data = request.form
    querie = login_account(
    data["email"],
    data["wachtwoord"])
    check_user = querie.search_user_database_user()
    if not check_user:
        return redirect(f"/login?correct={querie.correct}")
    else:
        session["user_type"] = check_user[0]
        session["user_id"] = check_user[1]
    return redirect("/")

@app.route("/login_check_organization", methods=["GET", "POST"])
def check_login_organization():
    # user type admin = beheerder, user type organization = organisatie, user type expert = ervaringsdeskundige
    if request.method == "GET":
        return redirect("/")
    data = request.form
    querie = login_account_organization(
    data["email"],
    data["phone"])
    check_organization = querie.search_user_database_organization()    
    if not check_organization:
        return redirect(f"/login?correct={querie.correct}")
    else:
        session["organization_name"] = check_organization[0]
        session["organization_id"] = check_organization[1]
        session["user_type"] = "organization"
    return redirect("/")
    
@app.route("/login")
def login_page():
    correct = request.args.get("correct")
    type_of_login = request.args.get("type_login")
    if type_of_login:
        session["type_login"] = type_of_login

    return render_template(
        "pages/login/login.html",
        page_title="Login",
        description="Login page",
        correct=correct
    )

@app.route("/logout")
def logout():
    return render_template("pages/login/logout.html", 
                           page_title="confirmatie uitloggen", 
                           description="Pagina om uit te loggen, klik op de uitloggen knop om uit te loggen.")

@app.route("/clear_session")
def clear_session():
    session.clear()
    return redirect("/")
    
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