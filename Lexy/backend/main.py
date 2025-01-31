from fastapi import FastAPI, UploadFile, File, HTTPException, Form, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from test_reading import get_pronunciation_errors

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    age = Column(Integer)
    wpm = Column(JSON, default=list)  
    wpm_count = Column(Integer, default=0)
    errors = Column(JSON, default=list) 

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic model for request validation
class UserCreate(BaseModel):
    username: str
    age: int

@app.post("/demo-signup")
async def create_user(user: UserCreate):
    db = SessionLocal()
    try:
        db_user = User(
            username=user.username,
            age=user.age,
            wpm=[],
            wpm_count=0,
            errors=[]
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {
            "id": db_user.id,
            "username": db_user.username
        }
    finally:
        db.close()


@app.post("/test-reading")
async def assess_reading(
    file: UploadFile = File(...), 
    text: str = Form(...),
    user_id: int = Form(...)
):
    # Create tmp directory if it doesn't exist
    os.makedirs("tmp", exist_ok=True)
    
    # Save uploaded audio file
    audio_path = os.path.abspath("tmp/audio.wav")
    with open(audio_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Get Azure credentials
    subscription_key = os.getenv("AZURE_SUBSCRIPTION_KEY")
    region = os.getenv("AZURE_REGION")
    
    print (text)
    # Get pronunciation errors and duration
    errors, duration_seconds = get_pronunciation_errors(
        audio_file=audio_path,
        reference_text=text,
        subscription_key=subscription_key,
        region=region
    )
    
    # Calculate WPM
    word_count = len(text.split())
    wpm = int((word_count / duration_seconds) * 60)
    
    # Update user data in database
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        #print every user data
        print(user.wpm, user.errors)
        if user:
            # Append new WPM score to the list
            if not isinstance(user.wpm, list):
                user.wpm = []
            user.wpm.append(wpm)
            user.wpm_count += 1
            
            # Append new errors to the list
            if not isinstance(user.errors, list):
                user.errors = []
            user.errors.extend(errors)
            
            db.commit()
            
        result = {
            "wpm": wpm,
            "errors": errors,
        }
        print (result)
    finally:
        db.close()
        # Clean up the temporary file
        os.remove(audio_path)
    
    return result                                                                                     

