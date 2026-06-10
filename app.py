from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from config import Config
from database import db
from models import User, CarbonRecord

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash("Email already exists")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(
            password
        )

        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful")

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(
                url_for("dashboard")
            )

        flash("Invalid Email or Password")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():

    records = CarbonRecord.query.filter_by(
        user_id=current_user.id
    ).all()

    total_emission = sum(
        record.total for record in records
    )

    return render_template(
        "dashboard.html",
        records=records,
        total_emission=total_emission
    )


@app.route(
    "/calculate",
    methods=["POST"]
)
@login_required
def calculate():

    electricity = float(
        request.form["electricity"]
    )

    vehicle = float(
        request.form["vehicle"]
    )

    flights = float(
        request.form["flights"]
    )

    electricity_emission = electricity * 0.85
    vehicle_emission = vehicle * 0.21
    flight_emission = flights * 90

    total = (
        electricity_emission
        + vehicle_emission
        + flight_emission
    )

    record = CarbonRecord(
        user_id=current_user.id,
        electricity=electricity_emission,
        vehicle=vehicle_emission,
        flights=flight_emission,
        total=total,
        date=datetime.now()
    )

    db.session.add(record)
    db.session.commit()

    flash(
        "Carbon Record Added Successfully"
    )

    return redirect(
        url_for("dashboard")
    )


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )