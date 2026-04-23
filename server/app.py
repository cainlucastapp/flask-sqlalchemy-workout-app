from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


# Workout Routes

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    schema = WorkoutSchema(many=True)
    return make_response(jsonify(schema.dump(workouts)), 200)

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    schema = WorkoutSchema()
    return make_response(jsonify(schema.dump(workout)), 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    schema = WorkoutSchema()
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)
    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()
    return make_response(jsonify(schema.dump(workout)), 201)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({'message': f'Workout {id} deleted successfully'}), 200)


# Exercise Routes

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    schema = ExerciseSchema(many=True)
    return make_response(jsonify(schema.dump(exercises)), 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    schema = ExerciseSchema()
    return make_response(jsonify(schema.dump(exercise)), 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    schema = ExerciseSchema()
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)
    exercise = Exercise(**data)
    db.session.add(exercise)
    db.session.commit()
    return make_response(jsonify(schema.dump(exercise)), 201)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({'message': f'Exercise {id} deleted successfully'}), 200)


# WorkoutExercise Routes

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def create_workout_exercise(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    
    data = request.get_json()
    schema = WorkoutExerciseSchema()
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)
    
    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        **data
    )
    db.session.add(workout_exercise)
    db.session.commit()
    return make_response(jsonify(schema.dump(workout_exercise)), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)