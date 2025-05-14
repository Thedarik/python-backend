from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    coins = Column(Integer, default=0)
    ism = Column(String)
    familiya = Column(String)
    user_image = Column(String, nullable=True)  # optional image

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    difficulty = Column(Integer)
    coins_reward = Column(Integer)

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    answer = Column(String)
    status = Column(String, default="pending")
    submission_date = Column(String)