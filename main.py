from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from fastapi import Body
from schemas import Student, StudentSettings, TaskCreate, Task, SubmissionCreate, Submission, SubmissionEvaluate
import crud

app = FastAPI(title="Student Coin System API")
Base.metadata.create_all(bind=engine)

@app.post("/register", response_model=Student)
def register(
    ism: str = Query(..., description="ism"),
    familiya: str = Query(..., description="familiya"),
    password: str = Query(..., description="password"),
    user_image: str = Query(None, description="user image (optional)"),  # optional
    db: Session = Depends(get_db)
):
    username = f"{ism.lower()}_{familiya.lower()}"
    db_student = crud.get_student_by_username(db, username)
    if db_student:
        raise HTTPException(status_code=400, detail="Bu ism va familiya bilan foydalanuvchi mavjud")
    return crud.create_student(db, ism, familiya, password, user_image)

@app.post("/login", response_model=Student)
def login(
    username: str = Query(..., description="username"),
    password: str = Query(..., description="password"),
    db: Session = Depends(get_db)
):
    db_student = crud.get_student_by_username(db, username)
    if not db_student or db_student.password_hash != crud.hash_password(password):
        raise HTTPException(status_code=401, detail="Noto‘g‘ri username yoki parol")
    return db_student

@app.post("/settings", response_model=Student)
def update_settings(
    username: str = Query(..., description="Eski username"),
    new_username: str = Query(..., description="Yangi username"),
    ism: str = Query(None, description="Yangi ism"),
    familiya: str = Query(None, description="Yangi familiya"),
    password: str = Query(None, description="Yangi parol"),
    user_image: str = Query(None, description="Image (optional)"),
    db: Session = Depends(get_db)
):
    db_student = crud.get_student_by_username(db, username)
    if not db_student:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    try:
        updated = crud.update_student_settings_query(
            db, username, new_username, ism, familiya, password, user_image
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/user/coins", response_model=Student)
def get_user_coins(
    username: str = Query(..., description="username"),
    db: Session = Depends(get_db)
):
    db_student = crud.get_student_coins(db, username)
    if not db_student:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return db_student

@app.get("/all/users/coins", response_model=list[Student])
def get_all_users_coins(db: Session = Depends(get_db)):
    return crud.get_all_students_coins(db)

@app.get("/user/settings", response_model=Student)
def get_user_settings(
    username: str = Query(..., description="username"),
    db: Session = Depends(get_db)
):
    db_student = crud.get_student_by_username(db, username)
    if not db_student:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return db_student

@app.post("/submit-task", response_model=Submission)
def submit_task(submission: SubmissionCreate, db: Session = Depends(get_db)):
    return crud.create_submission(db, submission)