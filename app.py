import os
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
import uuid
from flask import Flask, render_template, request, redirect, url_for

load_dotenv()
app = Flask(__name__)
client = MongoClient(os.environ.get("MONGODB_URI"))
db = client.Todo

@app.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3,4)]
        return dates
    
    return {"date_range": date_range}



@app.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = datetime.datetime.today()
        
    habits_on_date = db.Todo.find({"added": {"$lte":selected_date}})    
    Completed = [habit["habit"] for habit in db.Completed.find({"date":selected_date})]    
    return render_template("home.html",
                           habits=habits_on_date,
                           title="Let's Do IT - Home",
                           completions=Completed,
                           selected_date=selected_date)



@app.route("/add",  methods=["POST", "GET"])
def add_habit():

    
    if request.method == "POST":
       db.Todo.insert_one(
           {"_id":uuid.uuid4().hex, "added": datetime.datetime.today(), "name": request.form.get("habit")}
       )
    return render_template("todo.html",
                           title="Let's Do IT - Add Habit",
                           selected_date=datetime.datetime.today())


@app.route("/complete", methods=["POST"])
def complete():
    date_string = request.form.get("date")
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_string)
    db.Completed.insert_one({"date": date, "habit":habit})
    return redirect(url_for("index",date=date_string))


if __name__ == "__main__":
    app.run(host:="0.0.0.0", port:=int(os.environ.get('PORT', 5000)))