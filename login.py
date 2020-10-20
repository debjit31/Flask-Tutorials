
## Practice of tutorial 1 to 5
## creating a minimalistic login page with the concept of  sessions

from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta

app = Flask("__main__")
app.secret_key = "my_secret_key"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        ## perform the login here
        session.permanent = True
        user = request.form['nm']
        session['user'] = user
        return redirect(url_for("user"))
    else:
        ## check for login status
        if "user" in session:
            return redirect(url_for("user"))
        else:
            return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>Hello {user}</h1>"
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)



