import os
from flask import Flask, render_template
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
    return render_template("pages/index.html", counts=counts, page_title="Home")

@app.route("/ervaringsdeskunidge_dashboard")
def ervaringsdeskunidge_dashboard():
    return render_template("pages/ervaringsDeskundigeDashboard.html", page_title="dashboard")

@app.route("/register")
def register_page():
    return render_template("pages/login/register.html", page_title="Register")

@app.route("/login")
def login_page():
    return render_template("pages/login/login.html", page_title="Login")


if __name__ == "__main__":
    app.run(debug=True)
