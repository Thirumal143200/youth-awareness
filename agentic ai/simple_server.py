#!/usr/bin/env python3
"""
Simple working server for StromBreaker
"""

import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

class StromBreakerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        print(f"GET request: {self.path}")
        
        if self.path == '/':
            self.serve_file('index.html')
        elif self.path == '/chat.html':
            self.serve_file('chat.html')
        elif self.path == '/styles.css':
            self.serve_file('styles.css', 'text/css')
        elif self.path == '/script.js':
            self.serve_file('script.js', 'application/javascript')
        elif self.path == '/chat.css':
            self.serve_file('chat.css', 'text/css')
        elif self.path == '/chat.js':
            self.serve_file('chat.js', 'application/javascript')
        elif self.path == '/api/meditation/5':
            self.serve_api_meditation()
        elif self.path == '/api/journaling-prompts':
            self.serve_api_prompts()
        else:
            super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        print(f"POST request: {self.path}")
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        if self.path == '/api/chat':
            self.serve_api_chat(data)
        elif self.path == '/api/mood':
            self.serve_api_mood(data)
        elif self.path == '/api/activities':
            self.serve_api_activities(data)
        else:
            self.send_error(404)
    
    def serve_file(self, filename, content_type='text/html'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404)
    
    def serve_api_chat(self, data):
        message = data.get('message', '').lower()
        user_id = data.get('user_id', 'demo_user')
        
        print(f"Chat message: {message}")
        
        # Simple responses based on keywords
        if any(word in message for word in ['anxious', 'worried', 'scared', 'nervous', 'stress']):
            response = "I understand you're feeling anxious. Let's try some breathing exercises together. Take a deep breath in for 4 counts, hold for 4 counts, and exhale slowly for 6 counts. Repeat this and notice how your body feels calmer."
            mood_score = -0.5
            mood_label = "anxious"
            activities = ["Deep breathing exercise", "Guided meditation", "Write in your journal"]
        elif any(word in message for word in ['help', 'need', 'support', 'struggling']):
            response = "I'm here to support you. You're not alone in this. Sometimes talking about our feelings can help us feel better. What's on your mind?"
            mood_score = -0.3
            mood_label = "seeking support"
            activities = ["Talk to someone you trust", "Write about your feelings", "Take a mindful break"]
        elif any(word in message for word in ['meditate', 'meditation', 'calm', 'peace']):
            response = "Great choice! Meditation can help you find inner peace. Let's start with a simple 5-minute session. Find a comfortable position and focus on your breathing."
            mood_score = 0.3
            mood_label = "seeking calm"
            activities = ["Guided meditation", "Breathing exercise", "Mindful walking"]
        elif any(word in message for word in ['great', 'good', 'happy', 'amazing', 'wonderful', 'excellent']):
            response = "That's wonderful! I'm so glad you're feeling great today. Positive energy is contagious - maybe you could share some of that good feeling with someone else?"
            mood_score = 0.8
            mood_label = "positive"
            activities = ["Share your positive energy", "Plan something fun", "Help someone else feel good"]
        elif any(word in message for word in ['sad', 'down', 'depressed', 'upset']):
            response = "I'm sorry you're feeling down. It's okay to feel sad sometimes. Remember, these feelings are temporary. Would you like to try some gentle activities to help lift your mood?"
            mood_score = -0.7
            mood_label = "sad"
            activities = ["Gentle stretching", "Listen to uplifting music", "Practice gratitude"]
        else:
            response = "Thank you for sharing that with me. How are you feeling right now? I'm here to listen and support you."
            mood_score = 0.0
            mood_label = "neutral"
            activities = ["Take a mindful moment", "Check in with yourself", "Practice self-compassion"]
        
        response_data = {
            "response": response,
            "mood_score": mood_score,
            "mood_label": mood_label,
            "suggested_activities": activities
        }
        
        self.send_json_response(response_data)
    
    def serve_api_mood(self, data):
        print(f"Mood data: {data}")
        response_data = {"message": "Mood logged successfully"}
        self.send_json_response(response_data)
    
    def serve_api_activities(self, data):
        print(f"Activity data: {data}")
        response_data = {"message": "Activity logged successfully"}
        self.send_json_response(response_data)
    
    def serve_api_meditation(self):
        script = """Find a comfortable position where you can sit or lie down. Close your eyes gently and take a deep breath in through your nose for 4 counts... 1... 2... 3... 4... 

Now hold your breath for 4 counts... 1... 2... 3... 4...

Now exhale slowly through your mouth for 6 counts... 1... 2... 3... 4... 5... 6...

Repeat this breathing pattern. With each breath, feel your body becoming more relaxed. Notice any tension leaving your muscles. You are safe, you are calm, you are in control.

If your mind wanders, gently bring your attention back to your breathing. This is normal and part of the practice."""
        
        response_data = {
            "duration": 5,
            "script": script,
            "type": "guided_meditation"
        }
        self.send_json_response(response_data)
    
    def serve_api_prompts(self):
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
        selected_prompts = random.sample(prompts, 3)
        
        response_data = {"prompts": selected_prompts}
        self.send_json_response(response_data)
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

if __name__ == "__main__":
    PORT = 8000
    
    print("🧠 Starting StromBreaker Server")
    print("=" * 50)
    print(f"🌐 Main Website: http://localhost:{PORT}")
    print(f"💬 Chat Interface: http://localhost:{PORT}/chat.html")
    print("🚀 Fully functional - Test the chat!")
    print("=" * 50)
    
    with socketserver.TCPServer(("", PORT), StromBreakerHandler) as httpd:
        print(f"✅ Server running on http://localhost:{PORT}")
        print("📱 Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
            httpd.shutdown()
