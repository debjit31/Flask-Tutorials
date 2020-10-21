
## Practice of tutorial 1 to 5
## creating a minimalistic login page with the concept of  sessions

from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        ## perform the login here
        session.permanent = True
        ## store user_name in session
        user_name = request.form['nm']
        session['user'] = user_name
        ## store user details in db
        found_user = Users.query.filter_by(name=user_name).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = Users(user_name, "")
            db.session.add(usr)
            db.session.commit()
        flash("Login Successfull!!")
        return redirect(url_for("user"))
    else:
        ## check for login status
        if "user" in session:
            flash("Already Logged In!!!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user_name = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = Users.query.filter_by(name=user_name).first()
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
    app.run(debug=True)



