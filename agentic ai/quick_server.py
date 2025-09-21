#!/usr/bin/env python3
import http.server
import socketserver
import json
import os

class QuickHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.serve_file('index.html', 'text/html')
        elif self.path == '/chat.html':
            self.serve_file('chat.html', 'text/html')
        elif self.path.endswith('.css'):
            self.serve_file(self.path[1:], 'text/css')
        elif self.path.endswith('.js'):
            self.serve_file(self.path[1:], 'application/javascript')
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            message = data.get('message', '').lower()
            
            if 'anxious' in message:
                response = "I understand you're feeling anxious. Let's try breathing: In for 4, hold for 4, out for 6. You're safe."
                mood = -0.5
            elif 'sad' in message:
                response = "I'm sorry you're feeling down. It's okay to feel sad. You're not alone."
                mood = -0.7
            elif 'happy' in message or 'good' in message:
                response = "That's wonderful! I'm so glad you're feeling good today!"
                mood = 0.8
            else:
                response = "Thank you for sharing. How can I support you today?"
                mood = 0.0
            
            result = {
                "response": response,
                "mood_score": mood,
                "mood_label": "detected",
                "suggested_activities": ["Breathing exercise", "Meditation"]
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def serve_file(self, filename, content_type):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except:
            self.send_error(404)

if __name__ == "__main__":
    PORT = 8000
    print("🚀 StromBreaker - WORKING NOW!")
    print(f"🌐 http://localhost:{PORT}")
    print(f"💬 http://localhost:{PORT}/chat.html")
    
    with socketserver.TCPServer(("", PORT), QuickHandler) as httpd:
        print("✅ Server running!")
        httpd.serve_forever()
