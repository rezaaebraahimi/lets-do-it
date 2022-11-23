from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def todo():
    return render_template("home.html", title="Lets Do IT - Home")



@app.route("/add",  methods=["GET", "POST"])
def add_habit():
    return render_template("todo.html", title="Lets Do IT - Add Habit")

