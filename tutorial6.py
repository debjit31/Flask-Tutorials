## Implementing a Login and Logout System using Flask as the backend
## Sessions are stored on the server in Flask
## Permanent Sessions
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "my_secret_key"
app.permanent_session_lifetime=timedelta(minutes=5)


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
    return redirect(url_for("login"))


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("new.html", user = user)
    else:
        flash("You are not Logged In!!")
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
