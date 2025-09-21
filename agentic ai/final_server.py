#!/usr/bin/env python3
import http.server
import socketserver
import json
import os

class FinalHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        print(f"GET: {self.path}")
        
        if self.path == '/':
            self.serve_file('index.html', 'text/html')
        elif self.path == '/chat.html':
            self.serve_file('simple_chat.html', 'text/html')
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
            
            if 'anxious' in message or 'worried' in message or 'stress' in message:
                response = "I understand you're feeling anxious. Let's try some stress relief activities together. Here's a breathing exercise: Breathe in slowly for 4 counts, hold for 4 counts, and exhale for 6 counts. Repeat this 3 times. You're safe and I'm here to support you. 🌸"
                activities = ["Deep breathing exercise", "Progressive muscle relaxation", "Guided meditation"]
            elif 'sad' in message or 'down' in message or 'depressed' in message:
                response = "I'm sorry you're feeling down. It's completely okay to feel sad sometimes. Remember, these feelings are temporary. You're not alone in this. Let's try some gentle activities to help lift your mood. 💙"
                activities = ["Gentle stretching", "Listen to uplifting music", "Practice gratitude journaling"]
            elif 'happy' in message or 'good' in message or 'great' in message or 'amazing' in message:
                response = "That's wonderful! I'm so glad you're feeling great today! Positive energy is contagious - maybe you could share some of that good feeling with someone else? What made you feel so good? Let's celebrate this positive moment! 🌟"
                activities = ["Share your positive energy", "Plan something fun", "Help someone else feel good"]
            elif 'help' in message or 'support' in message:
                response = "I'm here to support you. You're not alone in this. Sometimes talking about our feelings can help us feel better. This is a safe, anonymous space where you can express yourself without judgment. What's on your mind? I'm listening. 🤗"
                activities = ["Talk about your feelings", "Write in your journal", "Practice self-compassion"]
            elif 'meditate' in message or 'meditation' in message:
                response = "Great choice! Meditation can help you find inner peace. Let's start with a guided meditation: Find a comfortable position, close your eyes gently, and focus on your breathing. Inhale slowly... exhale slowly... Feel your body relaxing with each breath. 🧘‍♀️"
                activities = ["5-minute guided meditation", "Breathing exercise", "Mindful walking"]
            elif 'journal' in message or 'write' in message:
                response = "Journaling is a wonderful way to express yourself! Here are some prompts to get you started: 'What am I grateful for today?', 'How am I feeling right now?', 'What would I like to tell my future self?' This is your private space to explore your thoughts. ✍️"
                activities = ["Gratitude journaling", "Emotional expression", "Daily reflection"]
            elif 'motivat' in message or 'inspir' in message:
                response = "You have incredible strength within you! Remember: every challenge you face makes you stronger. You're capable of amazing things, and it's okay to take things one step at a time. You've got this! 💪"
                activities = ["Positive affirmations", "Goal setting", "Celebrate small wins"]
            elif 'habit' in message or 'routine' in message:
                response = "Building healthy habits is a journey! Start small and be patient with yourself. What's one small thing you'd like to do for your mental wellness today? Remember, progress over perfection! 🌱"
                activities = ["Morning routine planning", "Habit tracking", "Wellness reminders"]
            else:
                response = "Thank you for sharing that with me. How are you feeling right now? I'm here to listen and support you on your wellness journey. This is your safe space to express yourself freely. What would help you feel better today? 💚"
                activities = ["Take a mindful moment", "Check in with yourself", "Practice self-care"]
            
            result = {
                "response": response,
                "mood_score": 0.0,
                "mood_label": "neutral",
                "suggested_activities": activities
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
        except Exception as e:
            print(f"Error serving {filename}: {e}")
            self.send_error(404)

if __name__ == "__main__":
    PORT = 8000
    print("🧠 StromBreaker - FINAL WORKING VERSION!")
    print("=" * 50)
    print(f"🌐 Main Site: http://localhost:{PORT}")
    print(f"💬 CHAT: http://localhost:{PORT}/chat.html")
    print("✅ GUARANTEED TO WORK!")
    print("=" * 50)
    
    with socketserver.TCPServer(("", PORT), FinalHandler) as httpd:
        print("🚀 Server running!")
        print("📱 Open your browser NOW!")
        httpd.serve_forever()
