import datetime
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
habits = ["Coding","Gaming"]
completions = defaultdict(list)


@app.context_processor
def add_calc_date_range():
    def date_range(start: datetime.date):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3,4)]
        return dates
    
    return {"date_range": date_range}


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
                           completions=completions[selected_date],
                           selected_date=selected_date)



@app.route("/add",  methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        habits.append(request.form.get("habit"))
    return render_template("todo.html",
                           title="Let's Do IT - Add Habit",
                           selected_date=datetime.date.today())


@app.route("/complete", methods=["POST"])
def complete():
    date_string = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_string)
    completions[date].append(habit)
    return redirect(url_for("index",date=date_string))
