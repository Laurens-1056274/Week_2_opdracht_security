# Beveiligingswijzigingen en installatie

Dit archief behoudt de oorspronkelijke mappenstructuur en originele bestanden.

## Voorbereiding

Gebruik Python 3.13 en `pip install -r requirements.txt`. Stel `FLASK_SECRET_KEY` in als een sterke willekeurige waarde (minimaal 32 tekens). Op PowerShell bijvoorbeeld:

`$env:FLASK_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"`

LET OP: bovenstaande PowerShell-expressie voert python niet automatisch uit als stringwaarde; gebruik:

`$env:FLASK_SECRET_KEY = (python -c "import secrets; print(secrets.token_urlsafe(48))")`

Gebruik HTTPS in productie en zet `FLASK_COOKIE_SECURE=1`.

## Bestaande database

Een bestaande database met plaintext wachtwoorden moet worden gemigreerd: draai eerst `python migrate_passwords.py` met een backup van de database. Het oude organisatie-inloggen met telefoonnummer vervalt. Voor bestaande organisatieaccounts is een wachtwoordherstel/nieuw wachtwoord nodig. Nieuwe organisatieaccounts krijgen nu een gebruikersaccount met gehasht wachtwoord.

## Nog te controleren

Test het aanmelden als admin, expert en organisatie, POST-formulieren, CSRF en beheerdersroutes. Voor productie zijn onder meer rate limiting, veilige wachtwoordreset en uitgebreide acceptatietests aanbevolen. De repository-zip bevat geen actieve app.db; deze moet lokaal bestaan of door de applicatie worden aangemaakt. De voorbeeldgebruikers hebben standaardwachtwoorden en zijn uitsluitend geschikt voor lokale demonstraties.
