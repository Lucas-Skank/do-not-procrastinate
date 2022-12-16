"""Main file of the application."""

from flask import Flask, redirect, render_template, request
from flask_login import login_required, current_user, login_user, logout_user
from models import User, Tasks, Rules, db, login
from utils import sum_points, filter_positive, filter_negative


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
    # If the current user is already authenticathed, redirect to the home page
    if current_user.is_authenticated:
        return redirect('/home')

    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in the user.

    If the user is already registered, it should redirect to the home page.
    If the user is not registered, redirect the user to the register page.
    """
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

    return redirect("/")


@app.route("/logout")
def logout():
    """Handle user logout"""
    logout_user()
    return redirect("/")


@app.route("/home")
def home():
    """Handle the home page of the app"""

    # Get data for that user
    userdata = {
        "id": current_user.id,
        "name": current_user.name,
        "username": current_user.username,
        "goal": current_user.goal,
    }

    userdata["user_rules"] = Rules.query.filter_by(user_id=current_user.id).all()

    # Get user tasks
    userdata["tasks"] = Tasks.query.filter_by(user_id=current_user.id).all()

    # Get positive points
    positive_tasks = filter_positive(userdata["tasks"])

    # Sum positive points
    userdata["positive_points"] = sum_points(positive_tasks)

    # Get negative points
    negative_tasks = filter_negative(userdata["tasks"])

    # Sum negative points
    userdata["negative_points"] = sum_points(negative_tasks)

    # Sum all user points
    userdata["total_points"] = sum_points(userdata["tasks"])

    return render_template("home.html", userdata=userdata)


@app.route("/goal", methods=["GET", "POST"])
def goal():
    """Handle goal page, its definition and update"""

    # If GET method used, render update goal page
    if request.method == "GET":
        return render_template("goal.html")

    # In case of POST, update the goal value of the user
    # and redirect to home
    new_goal = request.form.get("goal")

    User.query.filter(User.id == current_user.id).update(
        {"goal": new_goal}, synchronize_session=False
    )
    db.session.commit()

    return redirect("/home")


@app.route("/rule", methods=["GET", "POST"])
def rule():
    """TODO"""
    # If GET method used, render rule page
    if request.method == "GET":
        user_rules = Rules.query.filter_by(user_id=current_user.id).all()

        return render_template("rule.html", user_rules=user_rules)

    # In case of POST
    # Get the user input
    new_rule_data = {
        "rule_name": request.form.get("rule_name"),
        "point": int(request.form.get("point")),
        "pn": request.form.get("pn"),
    }

    # Checks if the user input makes sense
    user_input_values = new_rule_data.values()
    if None in user_input_values or "" in user_input_values:
        print("WRONG RULE INTPUT")
        return redirect("/rule")

    # Make pn true or false for db
    new_rule_data["pn"] = True if new_rule_data["pn"] == "Positive" else False
    # Crete rule object to add to the database
    new_rule = Rules(
        user_id=current_user.id,
        rule=new_rule_data["rule_name"],
        point=(
            - abs(new_rule_data["point"]) if not new_rule_data["pn"]
            else new_rule_data["point"]
        ),
        pn=new_rule_data["pn"]
    )

    # Add object to session and commit
    db.session.add(new_rule)
    db.session.commit()

    return redirect("/rule")


@app.route("/task", methods=["GET", "POST"])
def task():
    """TODO"""
    # If GET method used, render task page
    if request.method == "GET":
        user_rules = Rules.query.filter_by(user_id=current_user.id).all()
        return render_template("task.html", user_rules=user_rules)

    # In case of POST
    # Get the user input
    task_id = request.form.get("new_task")
    new_task_comment = request.form.get("comment")

    # Get proper object from db because front is sending string
    # TODO -> can be fixed if front send it as object
    new_task_obj = Rules.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).one_or_none()

    new_task = Tasks(
        user_id=current_user.id,
        task=new_task_obj.rule,
        point=new_task_obj.point,
        pn=new_task_obj.pn,
        comment=new_task_comment
    )

    # Add object to session and commit
    db.session.add(new_task)
    db.session.commit()

    return redirect("/home")


