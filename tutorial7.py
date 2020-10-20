## Implementing a Login and Logout System using Flask as the backend
## Sessions are stored on the server in Flask
## Permanent Sessions
## SQLAlchemy Database implemented
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite::///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime=timedelta(minutes=5)

db = SQLAlchemy(app)

## Create a SQLAlchemy database Model
class User(db.Model):
    ## Add columns to your table
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email
## Steps :-
## 1. Instantiate Flask
## 2. Setup the different routes for the website
## 3. each route is a function in python
## render the login template in the login route
## use sessions to save login data
## make the sessions temporarily permanent

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent =True
        user = request.form['nm']
        session["user"] = user
        flash("Login Successful!!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!!!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/logout")
def logout():
    ## delete a particular session
    if "user" in session:
        flash("You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/user", methods = ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email was saved!!!", "info")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email = email)
    else:
        flash("You are not Logged In!!")
        return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
