from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String())
    name = db.Column(db.String())
    goal = db.Column(db.String())

    tasks = db.relationship("Tasks", back_populates="users")
    rules = db.relationship("Rules", back_populates="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id"))
    task = db.Column(db.String())
    point = db.Column(db.Integer)
    comment = db.Column(db.String())
    pn = db.Column(db.Boolean)

    users = db.relationship("User", back_populates="tasks")


class Rules(db.Model):
    __tablename__ = 'rules'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id"))
    task = db.Column(db.String())
    point = db.Column(db.Integer)
    pn = db.Column(db.Boolean)

    users = db.relationship("User", back_populates="rules")
