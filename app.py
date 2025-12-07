import os
from flask import Flask, render_template,request,redirect
from data.database import Database
from models.user import User
from models.organization import Organization
from models.study import Study
from models.enrollment import Enrollment
from database_related_code.add_new_organisationaccount import submit_organisation_account
from database_related_code.login_user import login_account


app = Flask(__name__)

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
    counts = {
        "experts": users.count_all()[0],
        "organizations": organizations.count_all()[0],
        "studies": studies.count_all()[0],
        "enrollments": enrollments.count_all()[0],
    }
    return render_template("pages/index.html", 
                           counts=counts, 
                           page_title="Home",
                           description="Index Pagina")

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



@app.route("/login_check", methods=["GET", "POST"])
def check_login():
    if request.method == "GET":
        return redirect("/")
    data = request.form
    querie =login_account(
    data["email"],
    data["wachtwoord"]
    )
    check_user = querie.search_user_database()
    user_type = check_user
    return redirect(f"/login?correct={querie.correct}")

@app.route("/login")
def login_page():
    correct = request.args.get("correct")
    return render_template("pages/login/login.html", 
                           page_title="Login",
                           description="Login page",
                           correct=correct)

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
