from flask import Flask, render_template, request, jsonify
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'workout.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
db = SQLAlchemy(app)

class Workout(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   plan = db.Column(db.String(500), nullable=False)
with app.app_context():
   try:
      db.create_all()
   except Exception as e:
      print("Error when creating the dataset:", e)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/saveWorkout", methods=["POST"])
def save_workout():
   data = request.get_json()
   workout_plan = data.get('workoutPlan')
   new_workout = Workout(plan=workout_plan)
   db.session.add(new_workout)
   db.session.commit()
   return jsonify({"message": "Workout saved successfully!"})

@app.route("/getWorkouts", methods=["GET"])
def get_workouts():
   workouts = Workout.query.all()
   workout_list = [{"id": workout.id, "plan": workout.plan} for workout in workouts]
   return jsonify({"workouts": workout_list})


@app.route("/viewDatabase", methods=["GET"])
def view_database():
    workouts = Workout.query.all()
    workout_list = [{"id": workout.id, "plan": workout.plan} for workout in workouts]
    pprint(workout_list)
    return jsonify({"workouts": workout_list})

if __name__ == "__main__":
   port = int(os.environ.get("PORT", 5000))
   app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
