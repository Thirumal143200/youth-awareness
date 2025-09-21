🧠 StromBreaker - AI-Powered Youth Mental Wellness
A comprehensive Generative AI-powered mental wellness companion designed specifically for youth, providing 24/7 empathetic support, mood tracking, wellness activities, and gamified engagement.

🌟 Features
Core Functionality
AI-Driven Empathetic Chatbot - Context-aware conversational support
Real-time Mood Detection - Text and sentiment analysis
Wellness Activities - Guided meditation, breathing exercises, journaling
Progress Tracking - Comprehensive dashboard with insights
Gamification - Badges, streaks, and achievement system
Privacy-First - Anonymous, secure, stigma-free environment
Technical Features
Modern Web Interface - Responsive design with mobile support
Real-time Chat - WebSocket-based communication
Mood Analytics - Visual trend tracking and insights
Activity Logging - Comprehensive wellness activity tracking
Badge System - Achievement tracking and rewards
🚀 Quick Start
Prerequisites
Python 3.8+
OpenAI API Key (optional - demo mode available)
Installation
Clone the repository
git clone <repository-url>
cd strombreaker
Install dependencies
pip install -r requirements.txt
Set up environment variables
export OPENAI_API_KEY="your-openai-api-key-here"
Run the application
python run.py
Access the application
Main Website: http://localhost:8000
Chat Interface: http://localhost:8000/chat.html
API Documentation: http://localhost:8000/docs
🏗️ Architecture
Frontend
HTML5/CSS3 - Modern, responsive interface
JavaScript - Interactive features and real-time updates
Mobile-First Design - Optimized for all devices
Backend
FastAPI - High-performance Python web framework
SQLite - Local database for user data
OpenAI GPT - AI-powered conversational responses
RESTful API - Comprehensive API endpoints
Key Components
├── app.py              # FastAPI backend server
├── chat.html           # Interactive chat interface
├── chat.css            # Chat interface styling
├── chat.js             # Chat functionality
├── index.html          # Main website
├── styles.css          # Website styling
├── script.js           # Website interactions
├── requirements.txt    # Python dependencies
└── run.py              # Application launcher
📱 Usage
Chat Interface
Open http://localhost:8000/chat.html
Start chatting with StromBreaker AI
Use quick action buttons for common interactions
Track your mood using the mood tracker
Access wellness activities and meditation guides
Dashboard
View your mood trends over time
Track wellness activity streaks
See earned badges and achievements
Monitor your mental wellness journey
API Endpoints
POST /api/chat - Chat with AI
POST /api/mood - Log mood entries
POST /api/activities - Log wellness activities
GET /api/dashboard/{user_id} - Get dashboard data
GET /api/meditation/{duration} - Get meditation guides
GET /api/journaling-prompts - Get journaling prompts
🎯 Key Features in Detail
AI Chatbot
Context-aware responses using OpenAI GPT
Mood analysis and sentiment detection
Personalized activity suggestions
Empathetic, youth-friendly communication
Mood Tracking
5-point mood scale (Excellent to Struggling)
Visual mood trend charts
Optional notes and reflections
Historical mood data analysis
Wellness Activities
Guided Meditation - 5-15 minute sessions with scripts
Breathing Exercises - 4-7-8 breathing technique
Journaling - Prompts for self-reflection
Gratitude Practice - Daily gratitude exercises
Gamification
Daily streak tracking
Achievement badges
Progress milestones
Engagement rewards
🔧 Configuration
Environment Variables
OPENAI_API_KEY=your-openai-api-key-here  # Optional for AI features
DATABASE_URL=sqlite:///strombreaker.db   # Database configuration
Customization
Modify chat responses in app.py
Customize UI themes in CSS files
Add new wellness activities
Extend gamification features
📊 Data Privacy
Local Storage - User data stored locally
Anonymous Usage - No personal information required
Secure Communication - HTTPS-ready
Data Control - Users control their own data
🛠️ Development
Running in Development Mode
python run.py
API Testing
# Test chat endpoint
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "I feel anxious today"}'
Adding New Features
Backend: Add endpoints in app.py
Frontend: Update chat.js for new functionality
UI: Modify HTML/CSS for new components
🌍 UN SDG Alignment
This project aligns with UN Sustainable Development Goal 3: Good Health & Well-being

Promoting mental health awareness
Providing accessible mental wellness tools
Supporting youth mental health initiatives
Reducing stigma around mental health
👥 Team
StromBreaker Team

Team Leader: M. Mukesh Reddy
Focus: Youth Mental Wellness through AI
📄 License
This project is developed for hackathon purposes and educational use.

🤝 Contributing
Fork the repository
Create a feature branch
Make your changes
Test thoroughly
Submit a pull request
📞 Support
For questions or support, please contact the StromBreaker team.

StromBreaker - Breaking barriers in youth mental wellness through AI technology. 🧠✨
