import os
from flask import Flask, render_template,request,redirect,session,url_for
from data.database import Database
from models.registration_details import RegistratieDetails
from models.user import User
from models.organization import Organization
from models.study import Study
from models.enrollment import Enrollment
from models.registrations import Registratie
from database_related_code.add_new_organisationaccount import submit_organisation_account
from database_related_code.add_new_organisatieonderzoek import submit_organization_onderzoek
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
Registratie_model = Registratie('./app.db')
user_role_admin = False
user_role_organization = False
user_role_expert = False
db = Database("data/app.db")

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
    rows = enrollments.all_with_details()
    inschrijvingen = []
    for row in rows:
        inschrijvingen.append({
            "id": row[0],           
            "naam": row[1],        
            "organisatie": row[2],  
            "onderzoek": row[3],   
            "status": row[4],       
        })
    return render_template( "pages/beheerder/beheerder_inschrijvingen.html", 
                           page_title="BeheerderInschrijvingen",
                           inschrijvingen=inschrijvingen
    )
@app.route("/beheerder/inschrijvingen/<int:inschrijving_id>/goedkeuren")
def inschrijving_goedkeuren(inschrijving_id):
    enrollments.update_status(inschrijving_id, "goedgekeurd")
    return redirect(url_for("beheerder_inschrijvingen"))


@app.route("/beheerder/inschrijvingen/<int:inschrijving_id>/afkeuren")
def inschrijving_afkeuren(inschrijving_id):
    enrollments.update_status(inschrijving_id, "afgekeurd")
    return redirect(url_for("beheerder_inschrijvingen"))


@app.route("/registraties_overzicht", methods=["GET"])
def registraties_overzicht():
    registraties = Registratie_model.get_all_registraties()

    return render_template("pages/beheerder/registraties_overzicht.html",
                           page_title="Registraties overzicht",
                           description="Overzicht van nieuwe registraties",
                           registraties=registraties)

@app.route("/registratie_details/<int:profile_id>", methods=["GET"])
def registratie_details(profile_id):
    profile = Registratie_model.get_profile_details(profile_id)
    return render_template("pages/beheerder/registratie_details.html",
                           page_title="Registratie details",
                           description="Alle data van de deskundige",
                           profile=profile)

@app.route("/registratie/<int:profile_id>/goedkeuren", methods=["POST"])
def registratie_goedkeuren(profile_id):
    RegistratieDetails.update_status(profile_id, "goedgekeurd")
    return redirect(url_for("registraties_overzicht"))

@app.route("/registratie/<int:profile_id>/afkeuren", methods=["POST"])
def registratie_afkeuren(profile_id):
    RegistratieDetails.update_status(profile_id, "afgekeurd")
    return redirect(url_for("registraties_overzicht"))


@app.route("/ervaringsdeskunidge_dashboard")
def ervaringsdeskunidge_dashboard():
    return render_template("pages/beheerder/ervaringsDeskundigeDashboard.html", 
                           page_title="dashboard",
                           description="Ervarings Deskundige Dashboard")

@app.route("/login_check_user", methods=["GET", "POST"])
def check_login_user():
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

@app.route("/submit_study", methods=["POST"])
def submit_study():
    data = request.form
    organization_id = session.get("organization_id")

    has_reward = int(data.get("has_reward", 0))

    study_type = data.get("study_type", "online")
    if study_type not in ("telefonisch", "online", "op locatie"):
        study_type = "online"

    submit_organization_onderzoek(
        organization_id,
        data["title"],
        data.get("description", ""),
        data.get("start_date"),
        data.get("end_date"),
        study_type,
        data.get("location", ""),
        has_reward,
        data.get("reward", ""),
        data.get("age_min"),
        data.get("age_max")
    ).add_to_database()

    return redirect("/organisatie/onderzoeken")

@app.route("/onderzoeken")
def onderzoeken():
    conn = db.connect()
    beoordelen = conn.execute("""
    SELECT
      s.id, s.organization_id, s.title, s.status, s.available, s.description,
      s.start_date, s.end_date, s.study_type, s.location, s.has_reward, s.reward,
      s.age_min, s.age_max,
      o.name AS org_name
    FROM studies s
    JOIN organizations o ON o.id = s.organization_id
    ORDER BY s.start_date DESC
    """).fetchall()
    conn.close()

    return render_template("pages/beheerder/onderzoeken.html", beoordelen=beoordelen)

@app.route("/beheerder/onderzoeken/<int:onderzoek_id>/goedkeuren")
def onderzoek_goedkeuren(onderzoek_id):
    studies.update_status(onderzoek_id, "goedgekeurd")
    return redirect(url_for("onderzoeken"))    
    

@app.route("/beheerder/onderzoeken/<int:onderzoek_id>/afkeuren")
def onderzoek_afkeuren(onderzoek_id):
    studies.update_status(onderzoek_id, "afgekeurd")
    return redirect(url_for("onderzoeken"))

@app.route("/organisatie/onderzoeken")
def organisatie_onderzoeken():
    rows = studies.all_with_details()
    onderzoeken = []
    for row in rows:
        onderzoeken.append({
            "id": row["id"],            
            "organization_id": row["organization_id"],
            "organisatie": row["organisatie"],
            "title": row["title"],       
            "status": row["status"],       
            "available": row["available"],       
            "description": row["description"],       
            "start_date": row["start_date"],       
            "end_date": row["end_date"],       
            "study_type": row["study_type"],       
            "location": row["location"],       
            "has_reward": row["has_reward"],       
            "reward": row["reward"],       
            "age_min": row["age_min"],       
            "age_max": row["age_max"],       
        })
    return render_template(
        "pages/organisatie/organisatie_onderzoeken.html",
        page_title="Organisatie Onderzoek",
        description="Organisatie Onderzoek",
        onderzoeken=onderzoeken
    )


@app.route("/ervaringsdeskundige/inschrijvingen")
def ervaringsdeskundige_inschrijvingen():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    if session.get("user_type") != "expert":
        return redirect("/")
    profile_id = users.get_profile_id(user_id)
    if profile_id is None:
        return redirect("/")

    rows = enrollments.all_for_profile(profile_id)

    return render_template(
        "pages/ervaringsdeskundige/inschrijvingen.html",
        inschrijvingen=rows
    )
@app.route("/ervaringsdeskundige/profiel", methods=["GET", "POST"])
def ervaringsdeskundige_profiel():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    if session.get("user_type") != "expert":
        return redirect("/")
    if request.method == "POST":
        users.update_profile(
            user_id=user_id,
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            postcode=request.form.get("postcode"),
            phone=request.form.get("phone"),
            intro=request.form.get("intro")
        )
        return redirect("/ervaringsdeskundige/profiel")
    profiel = users.profile_by_user_id(user_id)
    if profiel is None:
        return redirect("/")

    return render_template(
        "pages/ervaringsdeskundige/profiel.html",
        profiel=profiel
    )


if __name__ == "__main__":
    app.run(debug=True)