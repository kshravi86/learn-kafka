from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from models import StudentCreate, StudentDisplay, Token, StudentUpdate
from auth import get_password_hash, verify_password
from database import fake_students_db

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Student CRUD API"}

@app.post("/register", response_model=StudentDisplay, status_code=201)
async def register_student(student: StudentCreate):
    if student.username in fake_students_db:
        raise HTTPException(status_code=409, detail="Username already registered")
    
    hashed_password = get_password_hash(student.password)
    
    # Create a dictionary that matches StudentDisplay structure (excluding password)
    # Pydantic models are preferred for structuring this data before storing if possible,
    # but for direct dict storage, ensure keys match.
    
    # Store the full student data including the hashed password
    student_data_db = student.model_dump() # Contains username, email, full_name, password
    student_data_db["hashed_password"] = get_password_hash(student.password)
    del student_data_db["password"] # Remove plain password before storing

    fake_students_db[student.username] = student_data_db
    
    # Return the stored student data; response_model=StudentDisplay will filter it.
    # StudentDisplay includes username, email, full_name from StudentBase.
    # It does not include password or hashed_password.
    return student_data_db

@app.post("/login") # You can add response_model=Token later if you implement full token logic
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_in_db = fake_students_db.get(form_data.username)
    if not user_in_db:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}, # Typically for token-based auth
        )
    
    # Ensure 'hashed_password' key exists and is used for verification
    hashed_password_in_db = user_in_db.get("hashed_password")
    if not hashed_password_in_db or not verify_password(form_data.password, hashed_password_in_db):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # For now, just a success message. Token generation would go here.
    # Example for future token:
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user_in_db["username"]}, expires_delta=access_token_expires
    # )
    # return {"access_token": access_token, "token_type": "bearer"}
    
    return {"message": "Login successful", "username": form_data.username}

@app.get("/students/{username}", response_model=StudentDisplay)
async def get_student_details(username: str):
    student_in_db = fake_students_db.get(username)
    if not student_in_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # StudentDisplay model will select the appropriate fields.
    # Ensure the data in fake_students_db can be mapped (e.g. no 'password' field directly,
    # and 'hashed_password' is not part of StudentDisplay)
    return student_in_db

@app.put("/students/{username}", response_model=StudentDisplay)
async def update_student_details(username: str, student_update: StudentUpdate):
    student_in_db = fake_students_db.get(username)
    if not student_in_db:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_update.model_dump(exclude_unset=True)
    
    # Update the stored student data
    student_in_db.update(update_data)
    # fake_students_db[username].update(update_data) # This also works if student_in_db is a reference

    return fake_students_db[username]

@app.delete("/students/{username}", status_code=status.HTTP_200_OK) # Or 204 if no content is returned
async def delete_student(username: str):
    if username not in fake_students_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    del fake_students_db[username]
    return {"message": "Student deleted successfully"} # Or return Response(status_code=status.HTTP_204_NO_CONTENT)
