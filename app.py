import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
import uuid


load_dotenv()
app = Flask(__name__)
app.secret_key = "letsdoit"
client = MongoClient(os.environ.get("MONGODB_URI"))
db = client.Todo


    ### Make a range list of dates ###

@app.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3,4)]
        return dates
    return {"date_range": date_range}


    ### define today format time ###

def today_():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)


    ### Main page function ###

@app.route("/", methods=["POST", "GET"])
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = today_()
            
    habits_on_date = db.Todo.find({"date": selected_date})
    Completed = [habit["name"] for habit in db.Completed.find(
                    {"date_complete":selected_date})]
    
    return render_template("home.html",
                           habits=habits_on_date,
                           title="Let's Do IT - Home",
                           completions=Completed,
                           selected_date=selected_date)


    ### when a task complete ###

@app.route("/complete", methods=["POST", "GET"])
def complete():
    date_string = request.form.get("date")
    date = datetime.datetime.fromisoformat(date_string)
    habit = request.form.get("habitName")
    db.Completed.insert_one({"date_complete": date, "name":habit})
    db.Todo.delete_one({"date": date, "name":habit})
    flash("Task Complete!", "warning")
    return redirect(url_for("index",date=date_string))


    ### add new daily task ###

@app.route("/add",  methods=["POST", "GET"])
def add_habit():
    today = today_()
    if request.form:
        db.Todo.insert_one({"_id":uuid.uuid4().hex,
                                    "date": today,
                                    "name": request.form.get("habit")})
        flash("New task successfully added!", "info")
        return redirect(url_for('index'))
    return render_template("todo.html",
                           title="Let's Do IT - Add Habit",
                           selected_date=today)


    ### show all of the completed tasks ###

@app.route("/show", methods = ["POST", "GET"])
def show():
    date_str = request.form.get("date") 
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = today_()
        
    habits_does = db.Completed.find({"date_complete": {"$lte":selected_date}}) 
    allcompleted = [
        habit["name"] for habit in db.Completed.find(
            {"date_complete":{"$lte":selected_date}})]
    
    return render_template("show.html",
                           title="Let's Do IT - Show All",
                           allcompleted=allcompleted,
                           habits_does=habits_does,
                           selected_date=selected_date)


    ### delete all of the completed tasks ###

@app.route('/delete_completed', methods = ["POST", "GET"])
def delete_completed():
    db.Completed.delete_many({})
    flash("Completed tasks has been deleted!", "error")
    return redirect(url_for('index'))

    ### Run App ###
if __name__ == "__main__":
    app.run(host:="0.0.0.0", port:=int(os.environ.get('PORT', 5000)))
