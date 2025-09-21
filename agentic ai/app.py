from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import openai
import os
from datetime import datetime, date
import json
import uuid
import sqlite3
from contextlib import asynccontextmanager
import asyncio

# Initialize FastAPI app
app = FastAPI(title="StromBreaker API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# OpenAI configuration
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
client = openai.OpenAI(api_key=openai.api_key)

# Database setup
DATABASE = "strombreaker.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            message TEXT,
            response TEXT,
            mood_score REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Mood tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_tracking (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            mood_score REAL,
            mood_label TEXT,
            notes TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Wellness activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wellness_activities (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            activity_type TEXT,
            duration INTEGER,
            completion_status TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Rewards table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rewards (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            badge_name TEXT,
            badge_description TEXT,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: str

class ChatMessage(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    mood_score: float
    mood_label: str
    suggested_activities: List[str]

class MoodEntry(BaseModel):
    user_id: str
    mood_score: float
    mood_label: str
    notes: Optional[str] = None

class WellnessActivity(BaseModel):
    user_id: str
    activity_type: str
    duration: int
    completion_status: str

class DashboardData(BaseModel):
    user_id: str
    mood_trend: List[dict]
    recent_activities: List[dict]
    badges_earned: List[dict]
    streak_count: int

# AI Chatbot Functions
async def analyze_mood(text: str) -> tuple:
    """Analyze mood from text using OpenAI"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mental health assistant. Analyze the emotional tone of the user's message and respond with a mood score from -1 (very negative) to 1 (very positive) and a mood label."},
                {"role": "user", "content": f"Analyze this message: '{text}'. Respond with JSON format: {{'mood_score': float, 'mood_label': str}}"}
            ],
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result['mood_score'], result['mood_label']
    except:
        return 0.0, "neutral"

async def generate_ai_response(message: str, mood_score: float, mood_label: str) -> tuple:
    """Generate empathetic AI response"""
    try:
        system_prompt = f"""
        You are StromBreaker, an empathetic AI companion for youth mental wellness. 
        The user's current mood is: {mood_label} (score: {mood_score})
        
        Guidelines:
        - Be empathetic, supportive, and non-judgmental
        - Use age-appropriate language for youth
        - Offer practical coping strategies
        - Suggest specific wellness activities when appropriate
        - Keep responses conversational and encouraging
        - Avoid giving medical advice
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        ai_response = response.choices[0].message.content
        
        # Generate suggested activities based on mood
        activities = await generate_suggested_activities(mood_score, mood_label)
        
        return ai_response, activities
    except Exception as e:
        return "I'm here to listen and support you. How are you feeling today?", []

async def generate_suggested_activities(mood_score: float, mood_label: str) -> List[str]:
    """Generate suggested wellness activities based on mood"""
    if mood_score < -0.5:
        return [
            "Deep breathing exercise (5 minutes)",
            "Guided meditation for stress relief",
            "Write in your journal about your feelings"
        ]
    elif mood_score < 0:
        return [
            "Quick mindfulness break",
            "Listen to calming music",
            "Take a short walk"
        ]
    elif mood_score < 0.5:
        return [
            "Gratitude journaling",
            "Light stretching exercises",
            "Connect with a friend"
        ]
    else:
        return [
            "Share your positive energy with others",
            "Plan something fun for later",
            "Help someone else feel good"
        ]

# Database functions
def get_db_connection():
    return sqlite3.connect(DATABASE)

def save_conversation(user_id: str, message: str, response: str, mood_score: float):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    conversation_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO conversations (id, user_id, message, response, mood_score)
        VALUES (?, ?, ?, ?, ?)
    ''', (conversation_id, user_id, message, response, mood_score))
    
    conn.commit()
    conn.close()

def save_mood_entry(user_id: str, mood_score: float, mood_label: str, notes: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    mood_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO mood_tracking (id, user_id, mood_score, mood_label, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (mood_id, user_id, mood_score, mood_label, notes))
    
    conn.commit()
    conn.close()

def get_user_mood_trend(user_id: str, days: int = 7) -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT mood_score, mood_label, timestamp
        FROM mood_tracking
        WHERE user_id = ? AND date(timestamp) >= date('now', '-{} days')
        ORDER BY timestamp DESC
    '''.format(days), (user_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "mood_score": row[0],
            "mood_label": row[1],
            "timestamp": row[2]
        }
        for row in results
    ]

def get_user_activities(user_id: str, limit: int = 10) -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT activity_type, duration, completion_status, timestamp
        FROM wellness_activities
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (user_id, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "activity_type": row[0],
            "duration": row[1],
            "completion_status": row[2],
            "timestamp": row[3]
        }
        for row in results
    ]

def get_user_badges(user_id: str) -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT badge_name, badge_description, earned_at
        FROM rewards
        WHERE user_id = ?
        ORDER BY earned_at DESC
    ''', (user_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "badge_name": row[0],
            "badge_description": row[1],
            "earned_at": row[2]
        }
        for row in results
    ]

def calculate_streak(user_id: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) FROM mood_tracking
        WHERE user_id = ? AND date(timestamp) >= date('now', '-30 days')
    ''', (user_id,))
    
    streak = cursor.fetchone()[0]
    conn.close()
    return streak

# API Routes
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "StromBreaker API - AI-Powered Youth Mental Wellness"}

@app.post("/api/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    user_id = str(uuid.uuid4())
    try:
        cursor.execute('''
            INSERT INTO users (id, username, email)
            VALUES (?, ?, ?)
        ''', (user_id, user.username, user.email))
        
        conn.commit()
        conn.close()
        
        return UserResponse(
            id=user_id,
            username=user.username,
            email=user.email,
            created_at=datetime.now().isoformat()
        )
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(chat_message: ChatMessage):
    try:
        # Analyze mood
        mood_score, mood_label = await analyze_mood(chat_message.message)
        
        # Generate AI response
        ai_response, suggested_activities = await generate_ai_response(
            chat_message.message, mood_score, mood_label
        )
        
        # Save conversation
        save_conversation(
            chat_message.user_id, 
            chat_message.message, 
            ai_response, 
            mood_score
        )
        
        # Save mood entry
        save_mood_entry(chat_message.user_id, mood_score, mood_label)
        
        return ChatResponse(
            response=ai_response,
            mood_score=mood_score,
            mood_label=mood_label,
            suggested_activities=suggested_activities
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/api/mood")
async def log_mood(mood_entry: MoodEntry):
    save_mood_entry(
        mood_entry.user_id,
        mood_entry.mood_score,
        mood_entry.mood_label,
        mood_entry.notes
    )
    return {"message": "Mood logged successfully"}

@app.post("/api/activities")
async def log_activity(activity: WellnessActivity):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    activity_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO wellness_activities (id, user_id, activity_type, duration, completion_status)
        VALUES (?, ?, ?, ?, ?)
    ''', (activity_id, activity.user_id, activity.activity_type, 
          activity.duration, activity.completion_status))
    
    conn.commit()
    conn.close()
    
    return {"message": "Activity logged successfully"}

@app.get("/api/dashboard/{user_id}", response_model=DashboardData)
async def get_dashboard_data(user_id: str):
    mood_trend = get_user_mood_trend(user_id)
    recent_activities = get_user_activities(user_id)
    badges_earned = get_user_badges(user_id)
    streak_count = calculate_streak(user_id)
    
    return DashboardData(
        user_id=user_id,
        mood_trend=mood_trend,
        recent_activities=recent_activities,
        badges_earned=badges_earned,
        streak_count=streak_count
    )

@app.get("/api/meditation/{duration}")
async def get_meditation_guide(duration: int = 5):
    """Generate guided meditation content"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Create a {duration}-minute guided meditation script for youth. Include breathing instructions, body relaxation, and positive affirmations. Keep it simple and encouraging."},
                {"role": "user", "content": f"Create a {duration}-minute meditation guide"}
            ],
            temperature=0.7
        )
        
        return {
            "duration": duration,
            "script": response.choices[0].message.content,
            "type": "guided_meditation"
        }
    except Exception as e:
        return {
            "duration": duration,
            "script": "Take a comfortable position. Close your eyes and focus on your breathing. Breathe in slowly for 4 counts, hold for 4 counts, and exhale for 6 counts. Repeat this cycle and let your mind find peace.",
            "type": "guided_meditation"
        }

@app.get("/api/journaling-prompts")
async def get_journaling_prompts():
    """Get random journaling prompts"""
    prompts = [
        "What are three things you're grateful for today?",
        "Describe a moment today when you felt proud of yourself.",
        "What's one challenge you faced today and how did you handle it?",
        "Write about someone who made you smile today.",
        "What's one thing you'd like to improve about your day tomorrow?",
        "Describe your ideal way to relax and unwind.",
        "What's a skill or hobby you'd like to learn?",
        "Write about a place that makes you feel calm and peaceful."
    ]
    
    import random
    return {
        "prompts": random.sample(prompts, 3)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
