from marshmallow import Schema, fields, validate

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