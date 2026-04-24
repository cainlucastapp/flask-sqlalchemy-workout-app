from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import *
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

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
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    schema = WorkoutSchema()
    return make_response(jsonify(schema.dump(workout)), 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({'error': 'No data provided'}), 400)
    schema = WorkoutSchema()
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)
    try:
        loaded_data = schema.load(data)
        workout = Workout(**loaded_data)
        db.session.add(workout)
        db.session.commit()
        return make_response(jsonify(schema.dump(workout)), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    try:
        db.session.delete(workout)
        db.session.commit()
        return make_response(jsonify({'message': f'Workout {id} deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)


# Exercise Routes

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    schema = ExerciseSchema(many=True)
    return make_response(jsonify(schema.dump(exercises)), 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    schema = ExerciseSchema()
    return make_response(jsonify(schema.dump(exercise)), 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({'error': 'No data provided'}), 400)
    schema = ExerciseSchema()
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)
    try:
        loaded_data = schema.load(data)
        exercise = Exercise(**loaded_data)
        db.session.add(exercise)
        db.session.commit()
        return make_response(jsonify(schema.dump(exercise)), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    try:
        db.session.delete(exercise)
        db.session.commit()
        return make_response(jsonify({'message': f'Exercise {id} deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)


# WorkoutExercise Routes

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def create_workout_exercise(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)

    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({'error': 'No data provided'}), 400)
    schema = WorkoutExerciseSchema()
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)
    try:
        loaded_data = schema.load(data)
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **loaded_data
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response(jsonify(schema.dump(workout_exercise)), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)


if __name__ == '__main__':
    app.run(port=5555, debug=True)