from marshmallow import Schema, fields, validate

# Marshmallow Schemas
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1, error="Reps must be greater than 0"))
    sets = fields.Int(validate=validate.Range(min=1, error="Sets must be greater than 0"))
    duration_seconds = fields.Int(validate=validate.Range(min=1, error="Duration must be greater than 0"))

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100, error="Name must be between 1 and 100 characters"))
    category = fields.Str(required=True, validate=validate.OneOf(
        ['weight training', 'cardio', 'yoga', 'spin', 'pilates', 'crossfit', 'other'],
        error="Invalid category"
    ))
    equipment_needed = fields.Bool(required=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, error="Duration must be greater than 0"))
    notes = fields.Str(validate=validate.Length(max=500, error="Notes cannot exceed 500 characters"))
    exercises = fields.List(fields.Nested(ExerciseSchema), dump_only=True)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)