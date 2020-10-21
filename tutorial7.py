## Implementing a Login and Logout System using Flask as the backend
## Sessions are stored on the server in Flask
## Permanent Sessions
## SQLAlchemy Database implemented
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime=timedelta(minutes=5)

db = SQLAlchemy(app)

## Create a SQLAlchemy database Model
class users(db.Model):
    ## Add columns to your table
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent =True
        user_name = request.form['nm']
        session["user"] = user_name
        ## save the user to the database
        found_user = users.query.filter_by(name=user_name).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user_name, "")
            db.session.add(usr)
            db.session.commit()

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
        user_name = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user_name).first()
            found_user.email = email
            db.session.commit()
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
