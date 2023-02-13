import uuid

from sqlalchemy import Column, ForeignKey, Integer, Double, Text, DateTime, UUID
from sqlalchemy.orm import relationship, Mapped

from ..database import Base
from .user import User
from .workout import Workout
from .exercise import Exercise


class Set(Base):
    __tablename__ = "sets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_time = Column(DateTime(timezone=True))
    weight = Column(Double, nullable=False)
    weight_unit = Column(Text, nullable=True)
    reps = Column(Integer, nullable=True)
    seconds = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    exercise_id = Column(UUID(as_uuid=True), ForeignKey("exercises.id"), nullable=False)
    exercise: Mapped[Exercise] = relationship("Exercise", backref="sets")

    workout_id = Column(UUID(as_uuid=True), ForeignKey("workouts.id"), nullable=False)
    workout: Mapped[Workout] = relationship("Workout", backref="sets")

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship("User", backref="sets")
