# Workout Tracker API

## Description
A RESTful backend API for a workout tracking application used by personal trainers. 
Built with Flask and SQLAlchemy, the API allows trainers to create and manage workouts, 
exercises, and track sets, reps, and duration for each exercise in a workout.

## Installation

### Prerequisites
- Python 3.14
- Pipenv

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd flask-sqlalchemy-workout-app
```

2. Install dependencies:
```bash
pipenv install
```

3. Navigate to the server directory:
```bash
cd server
```

4. Initialize and migrate the database:
```bash
python -m flask db init
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade head
```

5. Seed the database:
```bash
python seed.py
```

## Running the Application

```bash
cd server
python -m flask run --port=5555
```

The API will be available at `http://127.0.0.1:5555`

## Endpoints

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | Returns a list of all workouts with their associated exercises |
| GET | `/workouts/<id>` | Returns a single workout with its associated exercises and workout exercise data (sets/reps/duration) |
| POST | `/workouts` | Creates a new workout |
| DELETE | `/workouts/<id>` | Deletes a workout and its associated workout exercises |

#### POST /workouts request body:
```json
{
    "date": "2024-01-15",
    "duration_minutes": 60,
    "notes": "Morning strength session"
}
```

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | Returns a list of all exercises |
| GET | `/exercises/<id>` | Returns a single exercise and its associated workouts |
| POST | `/exercises` | Creates a new exercise |
| DELETE | `/exercises/<id>` | Deletes an exercise and its associated workout exercises |

#### POST /exercises request body:
```json
{
    "name": "Bench Press",
    "category": "weight training",
    "equipment_needed": true
}
```

#### Valid categories:
- weight training
- cardio
- yoga
- spin
- pilates
- crossfit
- other

### Workout Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Adds an exercise to a workout with sets, reps, and/or duration |

#### POST /workout_exercises request body:
```json
{
    "sets": 3,
    "reps": 12,
    "duration_seconds": null
}
```

## Dependencies
- Flask
- Flask-Migrate
- Flask-SQLAlchemy
- Werkzeug
- ipdb
- marshmallow