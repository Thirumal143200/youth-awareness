#!/usr/bin/env python3
"""
Simple demo server for StromBreaker
Runs without external dependencies for demonstration
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import sqlite3
import uuid
from datetime import datetime
import os

class StromBreakerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode())
        elif self.path == '/chat.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('chat.html', 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode())
        elif self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            super().do_POST()
    
    def handle_api_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        if self.path == '/api/chat':
            response = self.handle_chat(data)
        elif self.path == '/api/mood':
            response = self.handle_mood(data)
        elif self.path == '/api/activities':
            response = self.handle_activities(data)
        elif self.path == '/api/meditation/5':
            response = self.handle_meditation()
        elif self.path == '/api/journaling-prompts':
            response = self.handle_journaling_prompts()
        else:
            response = {"error": "Not found"}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def handle_chat(self, data):
        message = data.get('message', '')
        user_id = data.get('user_id', 'demo_user')
        
        # Simple demo responses
        responses = {
            'anxious': "I understand you're feeling anxious. Let's try some breathing exercises together. Breathe in for 4 counts, hold for 4, and exhale for 6 counts.",
            'help': "I'm here to support you. What's on your mind? Sometimes talking about our feelings can help us feel better.",
            'meditate': "Great choice! Let's start with a simple 5-minute meditation. Find a comfortable position and focus on your breathing.",
            'great': "That's wonderful! I'm so glad you're feeling great today. What made you feel so good?"
        }
        
        # Simple mood analysis
        mood_score = 0.0
        mood_label = "neutral"
        
        if any(word in message.lower() for word in ['anxious', 'worried', 'scared', 'nervous']):
            mood_score = -0.5
            mood_label = "anxious"
            response_text = responses.get('anxious', "I'm here to listen and support you.")
        elif any(word in message.lower() for word in ['help', 'need', 'support']):
            mood_score = -0.3
            mood_label = "seeking support"
            response_text = responses.get('help', "I'm here to help you through this.")
        elif any(word in message.lower() for word in ['meditate', 'meditation', 'calm']):
            mood_score = 0.3
            mood_label = "seeking calm"
            response_text = responses.get('meditate', "Meditation is a great way to find peace.")
        elif any(word in message.lower() for word in ['great', 'good', 'happy', 'amazing', 'wonderful']):
            mood_score = 0.8
            mood_label = "positive"
            response_text = responses.get('great', "I'm so happy you're feeling good!")
        else:
            response_text = "Thank you for sharing that with me. How are you feeling right now?"
        
        # Generate suggested activities
        activities = []
        if mood_score < 0:
            activities = ["Deep breathing exercise", "Guided meditation", "Write in your journal"]
        elif mood_score > 0.5:
            activities = ["Share your positive energy", "Plan something fun", "Help someone else"]
        else:
            activities = ["Take a mindful break", "Practice gratitude", "Connect with nature"]
        
        return {
            "response": response_text,
            "mood_score": mood_score,
            "mood_label": mood_label,
            "suggested_activities": activities
        }
    
    def handle_mood(self, data):
        return {"message": "Mood logged successfully"}
    
    def handle_activities(self, data):
        return {"message": "Activity logged successfully"}
    
    def handle_meditation(self):
        return {
            "duration": 5,
            "script": "Find a comfortable position. Close your eyes and focus on your breathing. Take a deep breath in for 4 counts, hold for 4 counts, and exhale slowly for 6 counts. Repeat this cycle and let your mind find peace. Notice how your body feels with each breath. You are safe, you are calm, you are in control.",
            "type": "guided_meditation"
        }
    
    def handle_journaling_prompts(self):
        prompts = [
            "What are three things you're grateful for today?",
            "Describe a moment today when you felt proud of yourself.",
            "What's one challenge you faced today and how did you handle it?",
            "Write about someone who made you smile today.",
            "What's one thing you'd like to improve about your day tomorrow?"
        ]
        import random
        return {"prompts": random.sample(prompts, 3)}

if __name__ == "__main__":
    print("🧠 Starting StromBreaker Demo Server")
    print("=" * 50)
    print("🌐 Main Website: http://localhost:8000")
    print("💬 Chat Interface: http://localhost:8000/chat.html")
    print("🚀 Demo mode - No OpenAI key required!")
    print("=" * 50)
    
    server = HTTPServer(('localhost', 8000), StromBreakerHandler)
    print("✅ Server running on http://localhost:8000")
    print("📱 Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()
