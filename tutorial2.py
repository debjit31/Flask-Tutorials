from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
myNames = ['Debjit', 'Anirban', 'Proloy']
@app.route("/<name>")
def home(name):
    return render_template("index.html", name = name, content = myNames)


if __name__ == "__main__":
    app.run()
