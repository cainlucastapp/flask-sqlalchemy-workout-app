from wsgiref import validate

from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', overlaps="workouts")
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', overlaps="workout_exercises")

    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == '':
            raise ValueError("Exercise name cannot be empty")
        return value

    @validates('category')
    def validate_category(self, key, value):
        allowed = ['weight training', 'cardio', 'yoga', 'spin', 'pilates', 'crossfit', 'other']
        if value.lower() not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(allowed)}")
        return value.lower()

    @validates('equipment_needed')
    def validate_equipment_needed(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("equipment_needed must be a boolean")
        return value



class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', overlaps="exercises")
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', overlaps="workout_exercises")

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be greater than 0")
        return value

    @validates('date')
    def validate_date(self, key, value):
        if not value:
            raise ValueError("Date cannot be empty")
        return value
    


# Join table for workouts and exercises
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises', overlaps="exercises,workouts")
    exercise = db.relationship('Exercise', back_populates='workout_exercises', overlaps="exercises,workouts")

    @validates('sets', 'reps')
    def validate_sets_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f"{key} must be greater than 0")
        return value

    @validates('duration_seconds')
    def validate_duration_seconds(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("duration_seconds must be greater than 0")
        return value
    

# Marshmallow Schemas
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int()
    exercise_id = fields.Int()
    reps = fields.Int(validate=validate.Range(min=1, error="Reps must be greater than 0"))
    sets = fields.Int(validate=validate.Range(min=1, error="Sets must be greater than 0"))
    duration_seconds = fields.Int(validate=validate.Range(min=1, error="Duration must be greater than 0"))

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, error="Name cannot be empty"))
    category = fields.Str(required=True, validate=validate.OneOf(
        ['weight training', 'cardio', 'yoga', 'spin', 'pilates', 'crossfit', 'other'],
        error="Invalid category"
    ))
    equipment_needed = fields.Bool(required=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, error="Duration must be greater than 0"))
    notes = fields.Str()
    exercises = fields.List(fields.Nested(ExerciseSchema), dump_only=True)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)