from flask import Flask, redirect, url_for

## instantiate an the WebApp
app = Flask(__name__)

## define routes for your project

## home page
@app.route("/")
def home():
    return "This is the Home Page!!<h1>HELLO</h1>"

## user page
@app.route("/<name>")
def user(name):
    return f"<h1>Hello {name}!</h1>"

## admin page
@app.route("/admin")
def admin():
    ## redirect functionality
    return redirect(url_for("home"))

## run the web app using a main function
if __name__ == "__main__":
    app.run()
