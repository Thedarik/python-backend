from sqlalchemy.orm import Session
from models import Student, Task, Submission
from schemas import TaskCreate, SubmissionCreate, StudentSettings
import hashlib
from datetime import datetime

DEFAULT_IMAGE_URL = "https://example.com/default-user.png"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_student(db: Session, ism: str, familiya: str, password: str, user_image: str = None):
    username = f"{ism.lower()}_{familiya.lower()}"
    db_student = Student(
        username=username,
        password_hash=hash_password(password),
        coins=0,
        ism=ism,
        familiya=familiya,
        user_image=user_image if user_image else DEFAULT_IMAGE_URL
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student_by_username(db: Session, username: str):
    return db.query(Student).filter(Student.username == username).first()

def update_student_settings_query(
    db: Session,
    current_username: str,
    new_username: str,
    ism: str = None,
    familiya: str = None,
    password: str = None,
    user_image: str = None
):
    db_student = get_student_by_username(db, current_username)
    if not db_student:
        return None

    # Username allaqachon mavjudmi?
    if new_username != current_username:
        existing = get_student_by_username(db, new_username)
        if existing:
            raise ValueError("Bu username allaqachon mavjud")
        db_student.username = new_username

    if ism:
        db_student.ism = ism
    if familiya:
        db_student.familiya = familiya
    if password:
        db_student.password_hash = hash_password(password)
    if user_image:
        db_student.user_image = user_image

    db.commit()
    db.refresh(db_student)
    return db_student



def get_student_coins(db: Session, username: str):
    return db.query(Student).filter(Student.username == username).first()

def get_all_students_coins(db: Session):
    return db.query(Student).order_by(Student.coins.desc()).all()

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def create_submission(db: Session, submission: SubmissionCreate):
    db_submission = Submission(
        **submission.dict(),
        status="pending",
        submission_date=datetime.now().isoformat()
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def evaluate_submission(db: Session, submission_id: int, status: str, coins: int):
    db_submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if db_submission:
        db_submission.status = status
        if status == "accepted":
            student = db.query(Student).filter(Student.id == db_submission.student_id).first()
            student.coins += coins
        db.commit()
        db.refresh(db_submission)
    return db_submission