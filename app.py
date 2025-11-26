import os
from flask import Flask, render_template,request,redirect
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
@app.route("/ede")
def index():
    counts = {
        "experts": users.count_all()[0],
        "organizations": organizations.count_all()[0],
        "studies": studies.count_all()[0],
        "enrollments": enrollments.count_all()[0],
    }
    return render_template("index.html", counts=counts)

@app.route("/")
def maak_account():
    return render_template("pages/beheerder/maak_organisatieaccount.html")

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
