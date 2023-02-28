from typing import Iterator
from datetime import datetime, timezone

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import delete
import pytest

from app.db.models.user import UserWithAuth
from app.db import Exercise, Workout, ExerciseType


@pytest.fixture(scope="function")
def postable_payload(
    primary_user_workout_and_exercise_type: tuple[Workout, ExerciseType]
):
    workout, exercise_type = primary_user_workout_and_exercise_type
    return {
        "start_time": "2023-01-01T12:00:00+00:00",
        "weight": 0,
        "reps": 25,
        "exercise_type_id": str(exercise_type.id),
        "workout_id": str(workout.id),
    }


@pytest.fixture(scope="function")
def primary_user_workout_and_exercise_type(
    session_factory: sessionmaker[Session],
    primary_test_user: UserWithAuth,
) -> Iterator[tuple[Workout, ExerciseType]]:
    user_id = primary_test_user.user.id
    with session_factory(expire_on_commit=False) as session:
        # Add a workout to record exercises in.
        wkt = Workout(
            start_time=datetime(2023, 1, 1, 8, 0, 0, tzinfo=timezone.utc),
            status="status",
            user_id=user_id,
        )
        # And an exercise type that exercises can be instances of.
        ex_tp = ExerciseType(
            name="Crunches",
            number_of_weights=0,
            owner_user_id=user_id,
        )
        session.add_all([wkt, ex_tp])
        session.commit()

    yield (wkt, ex_tp)

    with session_factory() as session:
        session.execute(delete(Workout).where(Workout.id == wkt.id))
        session.execute(delete(ExerciseType).where(ExerciseType.id == ex_tp.id))
        session.commit()


@pytest.fixture(scope="function")
def primary_user_exercises(
    session_factory: sessionmaker[Session],
    primary_test_user: UserWithAuth,
    primary_user_workout_and_exercise_type: tuple[Workout, ExerciseType],
) -> Iterator[tuple[Exercise, ...]]:
    """Add exercises owned by the primary user to the db."""
    user_id = primary_test_user.user.id
    workout, exercise_type = primary_user_workout_and_exercise_type
    with session_factory(expire_on_commit=False) as session:
        exes = [
            Exercise(
                start_time=datetime(2023, 1, 1, 10, 34, 3, tzinfo=timezone.utc),
                weight=10,
                weight_unit="Pounds",
                reps=25,
                notes="My first set of the day",
                exercise_type_id=exercise_type.id,
                workout_id=workout.id,
                user_id=user_id,
            ),
            Exercise(
                start_time=datetime(2023, 1, 1, 10, 35, 55, tzinfo=timezone.utc),
                weight=5,
                weight_unit="Pounds",
                reps=22,
                seconds=10,
                exercise_type_id=exercise_type.id,
                workout_id=workout.id,
                user_id=user_id,
            ),
        ]
        session.add_all(exes)
        session.commit()

    yield exes

    with session_factory() as session:
        session.execute(delete(Exercise).where(Exercise.id.in_(row.id for row in exes)))
        session.commit()