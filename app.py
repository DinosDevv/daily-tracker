from flask import Flask, render_template, request, redirect, jsonify
from fileutils import *
from datetime import date

app = Flask(__name__)

@app.route('/api/records')
def api_records():
    data = load_json('data/records.json')
    return jsonify(data)

def calculate_score(drinked: bool, smoked: int, exercised: bool, calories: int) -> float:
    # Normalize input values
    max_cals = 4000  # τυπικό upper limit
    max_smokes = 40  # υποθέτουμε το πολύ 40
    min_cals = 1000
    min_smokes = 1

    # Προστασία από μηδενικά
    smoked = max(smoked, min_smokes)
    calories = max(calories, min_cals)

    # Υπολογισμός υπο-βαθμών (όλοι στο range 0–1)
    drink_score = 1.0 if not drinked else 0.0
    exercise_score = 1.0 if exercised else 0.0
    calorie_score = 1.0 - (calories - min_cals) / (max_cals - min_cals)
    nicotine_penalty = 1.0 - (smoked - min_smokes) / (max_smokes - min_smokes)

    # Βάρη (προσαρμόσιμα)
    weights = {
        "drink": 0.25,
        "exercise": 0.25,
        "calories": 0.25,
        "nicotine": 0.25
    }

    final_score = (
        drink_score * weights["drink"] +
        exercise_score * weights["exercise"] +
        calorie_score * weights["calories"] +
        nicotine_penalty * weights["nicotine"]
    ) * 100

    return round(final_score, 2)


@app.route("/")
def home():
    return render_template('mainpage.html')

@app.route("/record-submition-form")
def record_form():
    return render_template('create-record.html')

def calculate_avg_score(data: list) -> str:
    total_score = 0
    avg_score = 0
    for entry in data:
        total_score += float(entry['score'])
    avg_score = round(total_score/(len(data)+1), 2) 

    if avg_score != 1:
        return str(avg_score)
    else: 
        return '0'

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
