from pydantic import BaseModel
from typing import Optional

class StudentSettings(BaseModel):
    new_username: str
    ism: Optional[str] = None
    familiya: Optional[str] = None
    password: Optional[str] = None
    user_image: Optional[str] = None



class Student(BaseModel):
    id: int
    username: str
    coins: int
    ism: str
    familiya: str
    user_image: Optional[str] = None

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    difficulty: int
    coins_reward: int

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    difficulty: int
    coins_reward: int

    class Config:
        from_attributes = True

class SubmissionCreate(BaseModel):
    student_id: int
    task_id: int
    answer: str

class SubmissionEvaluate(BaseModel):
    status: str
    coins: Optional[int] = 0

class Submission(BaseModel):
    id: int
    student_id: int
    task_id: int
    answer: str
    status: str
    submission_date: str

    class Config:
        from_attributes = True