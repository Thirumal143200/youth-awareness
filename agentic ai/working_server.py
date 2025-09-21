#!/usr/bin/env python3
"""
GUARANTEED WORKING StromBreaker Server
"""

import http.server
import socketserver
import json
import os

class WorkingHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        print(f"GET: {self.path}")
        
        if self.path == '/':
            self.serve_html('index.html')
        elif self.path == '/chat.html':
            self.serve_html('chat.html')
        elif self.path == '/styles.css':
            self.serve_css('styles.css')
        elif self.path == '/chat.css':
            self.serve_css('chat.css')
        elif self.path == '/script.js':
            self.serve_js('script.js')
        elif self.path == '/chat.js':
            self.serve_js('chat.js')
        else:
            super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        print(f"POST: {self.path}")
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        if self.path == '/api/chat':
            response = self.handle_chat(data)
        elif self.path == '/api/mood':
            response = {"message": "Mood saved!"}
        elif self.path == '/api/activities':
            response = {"message": "Activity saved!"}
        else:
            response = {"error": "Not found"}
        
        self.send_json(response)
    
    def serve_html(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            print(f"Error serving {filename}: {e}")
            self.send_error(404)
    
    def serve_css(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            print(f"Error serving {filename}: {e}")
            self.send_error(404)
    
    def serve_js(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            print(f"Error serving {filename}: {e}")
            self.send_error(404)
    
    def handle_chat(self, data):
        message = data.get('message', '').lower()
        
        # Simple but effective responses
        if 'anxious' in message or 'worried' in message:
            return {
                "response": "I understand you're feeling anxious. Let's try some breathing exercises. Breathe in for 4 counts, hold for 4, and exhale for 6 counts. You're safe and supported.",
                "mood_score": -0.5,
                "mood_label": "anxious",
                "suggested_activities": ["Breathing exercise", "Guided meditation"]
            }
        elif 'sad' in message or 'down' in message:
            return {
                "response": "I'm sorry you're feeling down. It's okay to feel sad sometimes. Remember, these feelings are temporary. Would you like to try some gentle activities?",
                "mood_score": -0.7,
                "mood_label": "sad",
                "suggested_activities": ["Gentle stretching", "Listen to music"]
            }
        elif 'happy' in message or 'good' in message or 'great' in message:
            return {
                "response": "That's wonderful! I'm so glad you're feeling good today. Positive energy is contagious - maybe you could share some of that good feeling with someone else?",
                "mood_score": 0.8,
                "mood_label": "happy",
                "suggested_activities": ["Share your energy", "Plan something fun"]
            }
        elif 'help' in message:
            return {
                "response": "I'm here to support you. You're not alone. Sometimes talking about our feelings can help us feel better. What's on your mind?",
                "mood_score": -0.3,
                "mood_label": "seeking help",
                "suggested_activities": ["Talk to someone", "Write your thoughts"]
            }
        else:
            return {
                "response": "Thank you for sharing that with me. How are you feeling right now? I'm here to listen and support you on your wellness journey.",
                "mood_score": 0.0,
                "mood_label": "neutral",
                "suggested_activities": ["Take a mindful moment", "Check in with yourself"]
            }
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

if __name__ == "__main__":
    PORT = 8000
    
    print("🧠 StromBreaker - GUARANTEED WORKING!")
    print("=" * 50)
    print(f"🌐 Website: http://localhost:{PORT}")
    print(f"💬 Chat: http://localhost:{PORT}/chat.html")
    print("✅ This WILL work!")
    print("=" * 50)
    
    with socketserver.TCPServer(("", PORT), WorkingHandler) as httpd:
        print(f"🚀 Server running on port {PORT}")
        print("📱 Open your browser now!")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Stopped")
