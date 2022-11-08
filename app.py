"""Main file of the application."""

from flask import Flask, redirect, render_template, request
from flask_login import login_required, current_user, login_user, logout_user
from models import User, db, login


app = Flask(__name__)
app.secret_key = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dnp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = "login"


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/")
def root():
    """Render login page to the user."""

    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in the user.

    If the user is already registered, it should redirect to the home page.
    If the user is not registered, redirect the user to the register page.
    """
    # If the current user is already authenticathed, redirect to the home page
    if current_user.is_authenticated:
        return redirect('/home')

    # Get the data passed by the user
    userdata = {
        "username": request.form.get("username"),
        "password": request.form.get("password")
    }

    # Verify if the user is already registered
    # Query for the user in the database
    user = User.query.filter_by(username=userdata["username"]).one_or_none()

    # If the query returns an user and the password matches, go home
    if user is not None and user.check_password(userdata["password"]):
        login_user(user)
        return redirect("/home")

    # If the user is not registered yet, load an error message
    msg = "User is not registered or credentials are wrong!"
    # The next page will redirect to `/` after 3 seconds
    return render_template("login_failed.html", msg=msg)


@app.route("/register", methods=["GET", "POST"])
def check_register():
    """Check user entry and register him if his data is correct.
    TODO -> better docstring
    """
    # If the current user is already authenticathed, redirect to the home page
    if current_user.is_authenticated:
        return redirect("/home")

    if request.method == "GET":
        return render_template("register.html")

    # In case of POST
    # Get the data passed by the user
    userdata = {
        "name": request.form.get("name"),
        "username": request.form.get("username"),
        "password": request.form.get("password"),
        "confpass": request.form.get("confpassword")
    }

    # Verify if the user is already registered
    user = User.query.filter_by(username=userdata["username"]).one_or_none()

    msg = None
    # If returns something, give an error that the user is already registered
    if user is not None:
        msg = "User is already registered!"
        return render_template("register_failed.html", msg=msg)

    # If returns nothing, save the user inside the database
    user = User(
        username=userdata["username"],
        name=userdata["name"],
    )
    user.set_password(userdata["password"])
    db.session.add(user)
    db.session.commit()
    return redirect("/login")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/home")
def home():
    """Handle the home page of the app"""
    # Get data for that user
    userdata = {
        "name": current_user.name,
        "username": current_user.username
    }

    return render_template("home.html", userdata=userdata)
