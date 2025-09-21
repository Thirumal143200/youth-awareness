#!/usr/bin/env python3
"""
StromBreaker - AI-Powered Youth Mental Wellness
Run script for the complete application
"""

import uvicorn
import os
from app import app

if __name__ == "__main__":
    # Set environment variables
    os.environ.setdefault("OPENAI_API_KEY", "your-openai-api-key-here")
    
    print("🧠 Starting StromBreaker - AI-Powered Youth Mental Wellness")
    print("=" * 60)
    print("🌐 Web Interface: http://localhost:8000")
    print("💬 Chat Interface: http://localhost:8000/chat.html")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    print("🚀 Server starting...")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )
