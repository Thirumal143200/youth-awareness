// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background change on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.problem-card, .feature-card, .team-card, .sdg-card, .flow-step');
    animatedElements.forEach(el => observer.observe(el));
});

// Chat simulation in phone mockup
function simulateChat() {
    const messages = [
        { type: 'ai', text: "Hi! I'm here to support your mental wellness journey. How are you feeling today?" },
        { type: 'user', text: "I'm feeling a bit stressed about exams..." },
        { type: 'ai', text: "I understand. Let's try a quick breathing exercise together. Ready?" },
        { type: 'user', text: "Sure, I'd like that." },
        { type: 'ai', text: "Great! Let's start with 4-7-8 breathing. Breathe in for 4 counts..." }
    ];
    
    const chatMessages = document.querySelector('.chat-messages');
    let messageIndex = 0;
    
    function addMessage() {
        if (messageIndex < messages.length) {
            const message = messages[messageIndex];
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${message.type}-message`;
            messageDiv.innerHTML = `<p>${message.text}</p>`;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            messageIndex++;
            setTimeout(addMessage, 2000);
        } else {
            // Reset after showing all messages
            setTimeout(() => {
                chatMessages.innerHTML = '';
                messageIndex = 0;
                setTimeout(addMessage, 1000);
            }, 5000);
        }
    }
    
    // Start the simulation
    setTimeout(addMessage, 1000);
}

// Start chat simulation when page loads
document.addEventListener('DOMContentLoaded', simulateChat);

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        const rate = scrolled * -0.5;
        hero.style.transform = `translateY(${rate}px)`;
    }
});

// Typing effect for hero title
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Initialize typing effect on page load
document.addEventListener('DOMContentLoaded', () => {
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const originalText = heroTitle.innerHTML;
        setTimeout(() => {
            typeWriter(heroTitle, originalText, 50);
        }, 500);
    }
});

// Counter animation for stats
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = counter.textContent;
        const isPercentage = target.includes('%');
        const isText = isNaN(target);
        
        if (!isText) {
            const finalNumber = parseInt(target);
            let current = 0;
            const increment = finalNumber / 50;
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= finalNumber) {
                    counter.textContent = target;
                    clearInterval(timer);
                } else {
                    counter.textContent = Math.floor(current) + (isPercentage ? '%' : '');
                }
            }, 30);
        }
    });
}

// Trigger counter animation when stats come into view
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounters();
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.addEventListener('DOMContentLoaded', () => {
    const statsSection = document.querySelector('.hero-stats');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
});

// Interactive feature cards
document.addEventListener('DOMContentLoaded', () => {
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Process flow step highlighting
document.addEventListener('DOMContentLoaded', () => {
    const flowSteps = document.querySelectorAll('.flow-step');
    
    flowSteps.forEach((step, index) => {
        step.addEventListener('mouseenter', () => {
            // Highlight current step and connected arrows
            step.style.background = 'linear-gradient(135deg, #6366f1, #8b5cf6)';
            step.style.color = 'white';
            step.style.transform = 'scale(1.1)';
        });
        
        step.addEventListener('mouseleave', () => {
            step.style.background = 'white';
            step.style.color = '#1e293b';
            step.style.transform = 'scale(1)';
        });
    });
});

// Tech stack item hover effects
document.addEventListener('DOMContentLoaded', () => {
    const techItems = document.querySelectorAll('.tech-item');
    
    techItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transform = 'scale(1.1)';
            item.style.background = '#4f46e5';
        });
        
        item.addEventListener('mouseleave', () => {
            item.style.transform = 'scale(1)';
            item.style.background = '#6366f1';
        });
    });
});

// Button click effects
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            button.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});

// Add ripple effect CSS
const style = document.createElement('style');
style.textContent = `
    .btn-primary, .btn-secondary {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Lazy loading for images (if any are added later)
const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            imageObserver.unobserve(img);
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const lazyImages = document.querySelectorAll('img[data-src]');
    lazyImages.forEach(img => imageObserver.observe(img));
});

// Console welcome message
console.log(`
🧠 StromBreaker - AI-Powered Youth Mental Wellness
==================================================
Built with ❤️ for youth mental health
Team Leader: M. Mukesh Reddy

Features:
• 24/7 AI-powered support
• Mood detection & analysis  
• Gamified wellness challenges
• Privacy-first approach
• Real-time progress tracking

Visit our website to learn more about our solution!
`);

// Performance monitoring
window.addEventListener('load', () => {
    const loadTime = performance.now();
    console.log(`Page loaded in ${Math.round(loadTime)}ms`);
});

// Error handling
window.addEventListener('error', (e) => {
    console.error('JavaScript error:', e.error);
});

// Service Worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Service worker can be added here for offline functionality
        console.log('Service Worker support detected');
    });
}
