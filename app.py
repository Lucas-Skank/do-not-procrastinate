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


@app.route("/login", methods=["POST"])
def login():
    """Log in the user.

    If the user is already registered, redirect him to the home page.
    If the user is not registered, redirect him to the register page.
    """
    # Get the data passed by the user
    userdata = {
        "username": request.form.get("username"),
        "password": request.form.get("password")
    }

    # Query for the user in the database
    user = User.query.filter_by(username=userdata["username"]).one_or_none()

    # If the query returns an user and the password matches, redirect to home
    if user is not None and user.check_password(userdata["password"]):
        login_user(user)
        return redirect("/home")

    return render_template("login_failed.html")


@app.route("/register", methods=["GET", "POST"])
def check_register():
    """Check user input from register page and save his data into the
    database.
    """
    # If the current user is already authenticathed, redirect to the home page
    if current_user.is_authenticated:
        return redirect("/home")

    # If GET method used, return register page
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
    # If query returns something, give an error that the user is already
    # registered
    if user is not None:
        msg = "User is already registered!"
        return render_template("register_failed.html", msg=msg)

    # If query returns nothing, save the user inside the database
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
    """Logout the user."""
    logout_user()
    return redirect("/")


@app.route("/home")
def home():
    """Load all necessary data to be used in home page and redirect the user
    to it.
    """
    # Get current user information
    userdata = {
        "id": current_user.id,
        "name": current_user.name,
        "username": current_user.username,
        "goal": current_user.goal,
    }

    userdata["user_rules"] = Rules.query.filter_by(
        user_id=current_user.id).all()

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


@app.route("/goal", methods=["POST"])
def goal():
    """Save user goal or update it."""
    # Update the goal value of the user and redirect to home
    new_goal = request.form.get("goal")

    User.query.filter(User.id == current_user.id).update(
        {"goal": new_goal}, synchronize_session=False
    )
    db.session.commit()

    return redirect("/home")


@app.route("/rule", methods=["GET", "POST"])
def rule():
    """Get user rule input, check it and save it to the database."""
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

    # Create rule object to add to the database
    new_rule = Rules(
        user_id=current_user.id,
        rule=new_rule_data["rule_name"],
        # Make the user input point a negative number
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


@app.route("/task", methods=["POST"])
def task():
    """Add new task into the database for the current user and redirect to
    home page."""
    # Get the user input
    task_id = request.form.get("new_task")
    task_comment = request.form.get("comment")

    # Get rule object to save it as task
    rule_obj = Rules.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).one_or_none()

    new_task = Tasks(
        user_id=current_user.id,
        task=rule_obj.rule,
        point=rule_obj.point,
        pn=rule_obj.pn,
        comment=task_comment
    )

    # Add object to session and commit
    db.session.add(new_task)
    db.session.commit()

    return redirect("/home")


@app.route("/delete", methods=["POST"])
def delete():
    """Delete a task or a rule from the database and redirect to home."""
    # Get input from the user
    task_id = request.form.get("task_id")
    rule_id = request.form.get("rule_id")

    # Get object to be deleted from the database
    if task_id is not None:
        obj = Tasks.query.filter_by(id=task_id).one_or_none()
    elif rule_id is not None:
        obj = Rules.query.filter_by(id=rule_id).one_or_none()

    # Delete object and commit to database
    db.session.delete(obj)
    db.session.commit()

    return redirect("/home")
