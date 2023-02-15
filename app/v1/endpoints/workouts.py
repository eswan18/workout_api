from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.sql import select
from sqlalchemy.orm import Session

from ..models.workout import WorkoutIn, WorkoutInDB
from app.v1.auth import get_current_user
from app import db

router = APIRouter(prefix="/workouts")


@router.get("/", response_model=list[WorkoutInDB])
def workouts(
    id: UUID | None = None,
    status: str | None = None,
    workout_type_id: UUID | None = None,
    session: Session = Depends(db.get_db),
    current_user: db.User = Depends(get_current_user),
) -> list[WorkoutInDB]:
    """
    Fetch all the workouts for your user.

    Not yet implemented: filtering by workout time. That'll be tricky since it needs to
    support gt/lt, not just equality.
    """
    query = select(db.Workout)

    # Filters
    eq_filters = {"id": id, "status": status, "workout_type_id": workout_type_id}
    # Ignore any that weren't provided.
    eq_filters = {
        key: value for (key, value) in eq_filters.items() if value is not None
    }
    query = query.filter_by(**eq_filters)

    # Permissions
    query = query.filter_by(user=current_user)

    result = session.scalars(query)
    records = [WorkoutInDB.from_orm(row) for row in result]
    return records


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WorkoutInDB)
def create_workout(
    workout: WorkoutIn,
    session: Session = Depends(db.get_db),
    current_user: db.User = Depends(get_current_user),
) -> db.Workout:
    """
    Record a new workout.
    """
    # Add the current user's ID to the record.
    workout_dict = workout.dict()
    workout_dict["user_id"] = current_user.id

    # Validate that the workout_type_id, if included, is present in the DB.
    workout_type_id = workout_dict["workout_type_id"]
    if workout_type_id is not None:
        if not db.model_id_exists(
            Model=db.WorkoutType, id=workout_type_id, session=session
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"workout type with id {workout_type_id} does not exist",
            )

    workout_record = db.Workout(**workout_dict)
    session.add(workout_record)
    session.commit()
    session.refresh(workout_record)
    return workout_record
