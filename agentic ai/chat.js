// StromBreaker Chat Application
class StromBreakerChat {
    constructor() {
        this.userId = this.getOrCreateUserId();
        this.isTyping = false;
        this.currentMood = null;
        this.meditationTimer = null;
        this.meditationDuration = 300; // 5 minutes in seconds
        this.meditationTimeLeft = this.meditationDuration;
        this.isMeditationActive = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadUserData();
        this.showWelcomeMessage();
    }
    
    getOrCreateUserId() {
        let userId = localStorage.getItem('strombreaker_user_id');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('strombreaker_user_id', userId);
        }
        return userId;
    }
    
    setupEventListeners() {
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.querySelector('.send-btn');
        
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        sendBtn.addEventListener('click', () => {
            this.sendMessage();
        });
        
        messageInput.addEventListener('input', () => {
            this.toggleSendButton();
        });
    }
    
    toggleSendButton() {
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.querySelector('.send-btn');
        
        if (messageInput.value.trim()) {
            sendBtn.disabled = false;
        } else {
            sendBtn.disabled = true;
        }
    }
    
    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        messageInput.value = '';
        this.toggleSendButton();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send to AI API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.userId,
                    message: message
                })
            });
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add AI response
            this.addMessage(data.response, 'ai');
            
            // Update mood if provided
            if (data.mood_score !== undefined) {
                this.updateMoodDisplay(data.mood_score, data.mood_label);
            }
            
            // Show suggested activities if provided
            if (data.suggested_activities && data.suggested_activities.length > 0) {
                this.showSuggestedActivities(data.suggested_activities);
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage("I'm sorry, I'm having trouble connecting right now. Please try again.", 'ai');
        }
    }
    
    addMessage(content, sender) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        if (sender === 'ai') {
            messageDiv.innerHTML = `
                <div class="ai-avatar-small">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>${content}</p>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <p>${content}</p>
                </div>
            `;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Auto-hide quick actions after first message
        if (document.querySelectorAll('.message').length > 1) {
            document.getElementById('quickActions').style.display = 'none';
        }
    }
    
    showTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        typingIndicator.style.display = 'flex';
    }
    
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        typingIndicator.style.display = 'none';
    }
    
    showWelcomeMessage() {
        // Welcome message is already in HTML
    }
    
    showSuggestedActivities(activities) {
        const chatMessages = document.getElementById('chatMessages');
        const activitiesDiv = document.createElement('div');
        activitiesDiv.className = 'message ai suggested-activities';
        
        let activitiesHTML = '<div class="ai-avatar-small"><i class="fas fa-lightbulb"></i></div><div class="message-content"><p>Here are some activities that might help:</p><div class="activity-suggestions">';
        
        activities.forEach(activity => {
            activitiesHTML += `<button class="activity-suggestion-btn" onclick="chat.sendQuickMessage('I want to try: ${activity}')">${activity}</button>`;
        });
        
        activitiesHTML += '</div></div>';
        activitiesDiv.innerHTML = activitiesHTML;
        
        chatMessages.appendChild(activitiesDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    updateMoodDisplay(moodScore, moodLabel) {
        // Update mood in header or show mood indicator
        console.log(`Mood updated: ${moodLabel} (${moodScore})`);
    }
    
    async loadUserData() {
        try {
            const response = await fetch(`/api/dashboard/${this.userId}`);
            const data = await response.json();
            
            // Update dashboard data
            document.getElementById('streakCount').textContent = data.streak_count || 0;
            this.updateMoodChart(data.mood_trend);
            this.updateActivitiesList(data.recent_activities);
            this.updateBadges(data.badges_earned);
            
        } catch (error) {
            console.error('Error loading user data:', error);
        }
    }
    
    updateMoodChart(moodTrend) {
        const canvas = document.getElementById('moodCanvas');
        const ctx = canvas.getContext('2d');
        
        // Simple mood chart
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        if (moodTrend.length === 0) return;
        
        const points = moodTrend.slice(0, 7); // Last 7 days
        const width = canvas.width;
        const height = canvas.height;
        const padding = 20;
        
        ctx.strokeStyle = '#6366f1';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        points.forEach((point, index) => {
            const x = padding + (index * (width - 2 * padding)) / (points.length - 1);
            const y = height - padding - (point.mood_score + 1) * (height - 2 * padding) / 2;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
    }
    
    updateActivitiesList(activities) {
        const activitiesList = document.getElementById('activitiesList');
        
        if (activities.length === 0) {
            activitiesList.innerHTML = '<p>No activities yet</p>';
            return;
        }
        
        let html = '';
        activities.slice(0, 5).forEach(activity => {
            const date = new Date(activity.timestamp).toLocaleDateString();
            html += `
                <div class="activity-item">
                    <span class="activity-type">${activity.activity_type}</span>
                    <span class="activity-date">${date}</span>
                </div>
            `;
        });
        
        activitiesList.innerHTML = html;
    }
    
    updateBadges(badges) {
        const badgesGrid = document.getElementById('badgesGrid');
        
        let html = '<div class="badge"><i class="fas fa-star"></i><span>New User</span></div>';
        
        badges.forEach(badge => {
            html += `
                <div class="badge">
                    <i class="fas fa-trophy"></i>
                    <span>${badge.badge_name}</span>
                </div>
            `;
        });
        
        badgesGrid.innerHTML = html;
    }
}

// Modal Functions
function openMoodTracker() {
    document.getElementById('moodModal').classList.add('show');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

function selectMood(score) {
    document.querySelectorAll('.mood-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    document.querySelector(`[data-mood="${score}"]`).classList.add('selected');
    chat.currentMood = score;
}

async function saveMood() {
    if (!chat.currentMood) {
        alert('Please select a mood first');
        return;
    }
    
    const notes = document.getElementById('moodNotes').value;
    const moodLabels = {
        1: 'struggling',
        2: 'down',
        3: 'okay',
        4: 'good',
        5: 'excellent'
    };
    
    try {
        await fetch('/api/mood', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: chat.userId,
                mood_score: chat.currentMood,
                mood_label: moodLabels[chat.currentMood],
                notes: notes
            })
        });
        
        closeModal('moodModal');
        chat.loadUserData(); // Refresh dashboard
        
        // Add confirmation message
        chat.addMessage(`Mood saved: ${moodLabels[chat.currentMood]}`, 'ai');
        
    } catch (error) {
        console.error('Error saving mood:', error);
        alert('Error saving mood. Please try again.');
    }
}

function openActivities() {
    document.getElementById('activitiesModal').classList.add('show');
}

function startActivity(type) {
    closeModal('activitiesModal');
    
    switch (type) {
        case 'meditation':
            startMeditation();
            break;
        case 'breathing':
            startBreathingExercise();
            break;
        case 'journaling':
            startJournaling();
            break;
        case 'gratitude':
            startGratitudePractice();
            break;
    }
}

async function startMeditation() {
    document.getElementById('meditationOverlay').style.display = 'flex';
    
    try {
        const response = await fetch('/api/meditation/5');
        const data = await response.json();
        document.getElementById('meditationScript').innerHTML = `<p>${data.script}</p>`;
    } catch (error) {
        console.error('Error loading meditation:', error);
    }
}

function toggleMeditation() {
    const playPauseBtn = document.querySelector('.play-pause-btn i');
    
    if (chat.isMeditationActive) {
        // Pause
        clearInterval(chat.meditationTimer);
        playPauseBtn.className = 'fas fa-play';
        chat.isMeditationActive = false;
    } else {
        // Play
        chat.meditationTimer = setInterval(updateMeditationTimer, 1000);
        playPauseBtn.className = 'fas fa-pause';
        chat.isMeditationActive = true;
    }
}

function updateMeditationTimer() {
    chat.meditationTimeLeft--;
    
    const minutes = Math.floor(chat.meditationTimeLeft / 60);
    const seconds = chat.meditationTimeLeft % 60;
    
    document.getElementById('meditationTimer').textContent = 
        `${minutes}:${seconds.toString().padStart(2, '0')}`;
    
    if (chat.meditationTimeLeft <= 0) {
        stopMeditation();
        chat.addMessage('Great job! You completed your meditation session. How do you feel?', 'ai');
    }
}

function stopMeditation() {
    clearInterval(chat.meditationTimer);
    chat.isMeditationActive = false;
    chat.meditationTimeLeft = chat.meditationDuration;
    document.getElementById('meditationTimer').textContent = '5:00';
    document.querySelector('.play-pause-btn i').className = 'fas fa-play';
    closeActivity();
    
    // Log activity
    logActivity('meditation', chat.meditationDuration);
}

function closeActivity() {
    document.getElementById('meditationOverlay').style.display = 'none';
}

async function startBreathingExercise() {
    chat.addMessage('Let\'s do a breathing exercise together. I\'ll guide you through 4-7-8 breathing.', 'ai');
    
    // Simulate breathing exercise
    setTimeout(() => {
        chat.addMessage('Breathe in slowly for 4 counts... 1... 2... 3... 4...', 'ai');
    }, 1000);
    
    setTimeout(() => {
        chat.addMessage('Hold your breath for 7 counts... 1... 2... 3... 4... 5... 6... 7...', 'ai');
    }, 6000);
    
    setTimeout(() => {
        chat.addMessage('Exhale slowly for 8 counts... 1... 2... 3... 4... 5... 6... 7... 8...', 'ai');
    }, 13000);
    
    setTimeout(() => {
        chat.addMessage('Great job! How do you feel after that breathing exercise?', 'ai');
    }, 21000);
    
    logActivity('breathing', 21);
}

async function startJournaling() {
    try {
        const response = await fetch('/api/journaling-prompts');
        const data = await response.json();
        
        chat.addMessage('Here are some journaling prompts to get you started:', 'ai');
        
        data.prompts.forEach((prompt, index) => {
            setTimeout(() => {
                chat.addMessage(`${index + 1}. ${prompt}`, 'ai');
            }, (index + 1) * 1000);
        });
        
        logActivity('journaling', 15);
    } catch (error) {
        chat.addMessage('Here are some journaling prompts: What are three things you\'re grateful for today?', 'ai');
    }
}

function startGratitudePractice() {
    chat.addMessage('Let\'s practice gratitude together. Think of three things you\'re grateful for today.', 'ai');
    
    setTimeout(() => {
        chat.addMessage('Take a moment to reflect on each one. How do they make you feel?', 'ai');
    }, 3000);
    
    setTimeout(() => {
        chat.addMessage('Gratitude practice can help shift your perspective and improve your mood. How was this exercise for you?', 'ai');
    }, 8000);
    
    logActivity('gratitude', 8);
}

async function logActivity(type, duration) {
    try {
        await fetch('/api/activities', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: chat.userId,
                activity_type: type,
                duration: duration,
                completion_status: 'completed'
            })
        });
        
        chat.loadUserData(); // Refresh dashboard
    } catch (error) {
        console.error('Error logging activity:', error);
    }
}

function openDashboard() {
    document.getElementById('dashboardModal').classList.add('show');
    chat.loadUserData(); // Refresh data when opening
}

// Quick message function
function sendQuickMessage(message) {
    document.getElementById('messageInput').value = message;
    chat.sendMessage();
}

// Initialize chat when page loads
let chat;
document.addEventListener('DOMContentLoaded', () => {
    chat = new StromBreakerChat();
});

// Close modals when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('show');
    }
});

// Handle meditation overlay clicks
document.getElementById('meditationOverlay').addEventListener('click', (e) => {
    if (e.target.id === 'meditationOverlay') {
        closeActivity();
    }
});
