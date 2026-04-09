from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, String, Text, Float, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    theme: Mapped[str] = mapped_column(String(50))  # 자연, 역사, 맛집 등
    title: Mapped[str] = mapped_column(String(200))
    explanation: Mapped[str] = mapped_column(Text)  # XAI 추천 사유
    total_distance_km: Mapped[float | None] = mapped_column(Float)
    estimated_minutes: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="courses")
    waypoints = relationship("CourseWaypoint", back_populates="course", order_by="CourseWaypoint.order")
    feedbacks = relationship("CourseFeedback", back_populates="course")


class CourseWaypoint(Base):
    __tablename__ = "course_waypoints"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    order: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(50))  # bike_station, tourist_spot
    location: Mapped[str] = mapped_column(Geometry("POINT", srid=4326))
    description: Mapped[str | None] = mapped_column(Text)

    course = relationship("Course", back_populates="waypoints")


class CourseFeedback(Base):
    __tablename__ = "course_feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rating: Mapped[int] = mapped_column(Integer)  # 1-5
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    course = relationship("Course", back_populates="feedbacks")
