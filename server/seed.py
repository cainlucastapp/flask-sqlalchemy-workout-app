#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():

    # Clear out all tables
    print("Clearing tables...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # Create Exercises
    print("Seeding exercises...")
    e1 = Exercise(name="Bench Press", category="weight training", equipment_needed=True)
    e2 = Exercise(name="Running", category="cardio", equipment_needed=False)
    e3 = Exercise(name="Downward Dog", category="yoga", equipment_needed=False)
    e4 = Exercise(name="Deadlift", category="weight training", equipment_needed=True)
    e5 = Exercise(name="Spin Class", category="spin", equipment_needed=True)

    db.session.add_all([e1, e2, e3, e4, e5])
    db.session.commit()

    # Create Workouts
    print("Seeding workouts...")
    w1 = Workout(date=date(2024, 1, 15), duration_minutes=60, notes="Morning strength session")
    w2 = Workout(date=date(2024, 1, 17), duration_minutes=45, notes="Cardio day")
    w3 = Workout(date=date(2024, 1, 19), duration_minutes=30, notes="Yoga and stretching")

    db.session.add_all([w1, w2, w3])
    db.session.commit()

    # Create WorkoutExercises
    print("Seeding workout exercises...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, sets=4, reps=10, duration_seconds=None)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e4.id, sets=3, reps=8, duration_seconds=None)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e2.id, sets=None, reps=None, duration_seconds=1800)
    we4 = WorkoutExercise(workout_id=w2.id, exercise_id=e5.id, sets=None, reps=None, duration_seconds=2700)
    we5 = WorkoutExercise(workout_id=w3.id, exercise_id=e3.id, sets=3, reps=None, duration_seconds=300)

    db.session.add_all([we1, we2, we3, we4, we5])
    db.session.commit()

    print("Done seeding!")