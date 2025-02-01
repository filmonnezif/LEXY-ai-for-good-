from fastapi import FastAPI, UploadFile, File, HTTPException, Form, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from test_reading import get_pronunciation_errors
from document_processer import extract_text_from_document
from audio_creator import AzureTextToSpeech
from prompts import word_replacement_prompt, voice_chat_prompt
from langchain_core.messages import HumanMessage
from LLM_source import llm , llm_groq
import json
import requests
from typing import Dict

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


@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """
    Endpoint to extract text from uploaded documents
    """
    # Read the file content
    content = await file.read()
    
    # Extract text from the document
    extracted_text = extract_text_from_document(content)
    print (extracted_text)
    
    return {"text": extracted_text}


class RemixRequest(BaseModel):
    words: list[str]
    document: str

@app.post("/remix")
async def remix_text(remix_request: RemixRequest):
    formatted_prompt = word_replacement_prompt.format(
        complex_words=remix_request.words,
        document=remix_request.document
    )
    user_message = HumanMessage(content=formatted_prompt)
    remix_response = llm.invoke([user_message])
    remixed_text = remix_response.content
    
    return {
        "remixed_text": remixed_text
    }


AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION") or "global"

class TranslationRequest(BaseModel):
    text: str

@app.post("/translate-to-arabic")
async def translate_to_arabic(translation_request: TranslationRequest):
    endpoint = "https://api.cognitive.microsofttranslator.com/translate"
    location = AZURE_TRANSLATOR_REGION
    
    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': 'ar'
    }
    
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json'
    }
    
    body = [{
        'text': translation_request.text
    }]
    
    response = requests.post(endpoint, params=params, headers=headers, json=body)
    translation_result = response.json()

    return {
        "translated_text": translation_result[0]["translations"][0]["text"]
    }

active_connections: Dict[int, WebSocket] = {}


@app.websocket("/ws/audio-chat/{user_id}")
async def audio_chat_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    document_context = ""
    
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            
            if data.get('type') == 'context':
                document_context = data['content']
                print ("context received")
                continue
                
            user_message = data.get('message', message)
            print (user_message)
            formatted_prompt = voice_chat_prompt.format(
                context=document_context,
                user_message=user_message
            )
            
            response = llm_groq.invoke(formatted_prompt)
            print(response.content)
            tts = AzureTextToSpeech()
            ssml_text = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                <voice name="en-US-AvaMultilingualNeural">
                {response.content}
                </voice>
                </speak>"""
            
            audio_path = "response.wav"
            tts.create_audio(ssml_text, output_path=audio_path, use_ssml=True)
            
            with open(audio_path, "rb") as audio_file:
                await websocket.send_bytes(audio_file.read())
            
            os.remove(audio_path)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if user_id in active_connections:
            del active_connections[user_id]