from flask import Flask, render_template, request, redirect
from fileutils import *
from datetime import date

app = Flask(__name__)

def calculate_score(drinked: bool, smoked: int, exercised: bool, calories: int) -> float:
    drink_score = 0
    exercise_score = 0

    if drinked:
        drink_score=0
    else:
        drink_score=1
    if exercised:
        exercise_score=1
    else:
        exercise_score=0

    return round(((drink_score*50)+(exercise_score*50) + (calories/100))/(smoked*0.1), 2)

@app.route("/")
def home():
    return render_template('mainpage.html')

@app.route("/record-submition-form")
def record_form():
    return render_template('create-record.html')

def calculate_avg_score(data: list) -> str:
    total_score = 0
    for entry in data:
        total_score += float(entry['score'])
    return str(round(total_score/len(data), 2))

def calculate_most_active(data: list) -> str:
    return '7/7/2025' #...
@app.route("/analytics")
def analytics():
    data = load_json('data/records.json')

    avg_score = calculate_avg_score(data)
    most_active = calculate_most_active(data)
    total_records = str(len(data))

    anal_info = {
        "avg_score": avg_score,
        "most_active": most_active,
        "total_records": total_records
    }
    return render_template('analytics.html', analytics_info=anal_info)

@app.route("/submit-record", methods=["GET", "POST"])
def save_record():
    
    drinked = "drink" in request.form
    smoked = int(request.form.get("nicotine", "").strip())
    exercised = "exercise" in request.form
    calories = int(request.form.get("calories", "").strip())
    weight = float(request.form.get("weight", "").strip())
    score = calculate_score(drinked, int(smoked), exercised, int(calories))

    data_to_pass = {
      "date": str(date.today()),
      "drinked": drinked,
      "smoked": smoked,
      "exercised": exercised,
      "calories": calories,
      "weight": weight,
      "score": score
    }

    save_json('data/records.json', data_to_pass)
    return redirect('/records')

@app.route("/records", methods=["GET"])
def records():
    data = load_json('data/records.json')
    return render_template('records.html', records=data)
  

@app.route("/clear", methods=["POST"])
def clear():
    clear_json('data/records.json')
    return redirect('/records')
if __name__ == "__main__":
    app.run(debug=True)
