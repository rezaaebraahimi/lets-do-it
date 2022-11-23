import datetime
from flask import Flask, render_template, request


app = Flask(__name__)
habits = ["Coding","Gaming"]

def date_range(start: datetime.date):
    dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
    return dates

@app.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()
        
    return render_template("home.html",
                           habits=habits,
                           title="Let's Do IT - Home",
                           date_range=date_range,
                           selected_date=selected_date)



@app.route("/add",  methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        habits.append(request.form.get("habit"))
    return render_template("todo.html", title="Let's Do IT - Add Habit")

