
import streamlit as st
from dotenv import load_dotenv
import requests
import os
import random
import time
import json

# Load environment variables
load_dotenv()
# Custom CSS with enhanced space theme
st.markdown("""
<style>
    /* Modern Space Theme */
    .main {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Glassmorphism Cards */
    .mission-card {
             color: black !important;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .mission-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.45);
    }
    
    /* Neon Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #FF4B91 30%, #FF7676 90%);
        color: white;
        font-weight: 600;
        border-radius: 30px;
        padding: 15px 30px;
        border: none;
        box-shadow: 0 0 15px rgba(255, 75, 145, 0.5);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 0 25px rgba(255, 75, 145, 0.7);
    }
    
    /* Progress Tracker */
    .progress-milestone {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        transition: all 0.3s ease;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .milestone-active {
        background: linear-gradient(45deg, #FF4B91, #FF7676);
        border-color: rgba(255, 255, 255, 0.3);
        animation: pulse 2s infinite;
    }
    
    /* Achievement Badge */
    .achievement-badge {
             color: black !important;
        font-size: 3em;
        text-align: center;
        margin: 15px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: float 3s ease-in-out infinite;
    }
    
    /* Quote Box */
    .quote-box {
            color: black !important;
        background: linear-gradient(135deg, rgba(255, 75, 145, 0.1), rgba(255, 118, 118, 0.1));
        border-left: 5px solid #FF4B91;
        padding: 20px;
        margin: 25px 0;
        border-radius: 0 20px 20px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Animations */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 75, 145, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 75, 145, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 75, 145, 0); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .mission-card {
            padding: 15px;
            margin: 10px 0;
        }
        
        .progress-milestone {
            width: 35px;
            height: 35px;
        }
        
        .achievement-badge {
            font-size: 2em;
            padding: 15px;
        }
    }
    
    /* Enhanced Text Styles */
    h1, h2, h3 {
        background: linear-gradient(120deg, #FF4B91, #FF7676);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #FF4B91, #FF7676);
        border-radius: 5px;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 15px !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
            color: black !important;
        border-color: #FF4B91 !important;
        box-shadow: 0 0 10px rgba(255, 75, 145, 0.3) !important;
    }
    
    /* Checkbox Custom Style */
    .stCheckbox>div>div>label {
        color: white !important;
    }
    
    /* Progress Bar */
    .stProgress>div>div>div {
        background: linear-gradient(45deg, #FF4B91, #FF7676) !important;
    }
</style>
""", unsafe_allow_html=True)

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/facebook/opt-350m"  # Using a more reliable model
headers = {"Authorization": f"Bearer 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"}

def query_huggingface(payload):
    try:
        # Simplify payload
        if isinstance(payload, dict):
            text = payload.get('inputs', '')
        else:
            text = str(payload)
            
        simple_payload = {
            "inputs": text,
            "options": {
                "wait_for_model": True
            }
        }
        
        # Make API request
        response = requests.post(API_URL, headers=headers, json=simple_payload)
        
        # Handle different response cases
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and result:
                return result[0].get('generated_text', '')
            return get_fallback_response(text)
            
        elif response.status_code == 503:
            st.warning("Model is loading... Please try again in a few seconds.")
            time.sleep(5)  # Wait for model to load
            return get_fallback_response(text)
            
        else:
            st.error(f"API Error: Status code {response.status_code}")
            return get_fallback_response(text)
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return get_fallback_response(text)

def test_api_connection():
    try:
        test_response = query_huggingface("Generate a short motivational message")
        if test_response and not test_response.startswith("API Error"):
            return True, "API connection successful!"
        return False, "API connection failed"
    except Exception as e:
        return False, f"Connection Error: {str(e)}"

# Add this at the start of your app to test the connection
with st.sidebar:
    if st.button("🔄 Test API Connection"):
        with st.spinner("Testing API connection..."):
            is_connected, message = test_api_connection()
            if is_connected:
                st.success(message)
            else:
                st.error(message)

def get_fallback_response(prompt):
    responses = {
        "mission": [
            "Embark on a journey of continuous learning and growth.",
            "Push beyond your current limits and explore new possibilities.",
            "Transform challenges into opportunities for advancement."
        ],
        "challenge": [
            "Break down your mission into daily explorations.",
            "Track your progress like a space mission - one milestone at a time.",
            "Maintain mission logs to document your growth journey."
        ],
        "motivation": [
            "The universe of possibilities awaits your exploration.",
            "Every small step is a leap toward your greater potential.",
            "Your growth journey is as vast as space itself."
        ]
    }
    
    if "mission" in prompt.lower():
        return random.choice(responses["mission"])
    elif "challenge" in prompt.lower():
        return random.choice(responses["challenge"])
    else:
        return random.choice(responses["motivation"])

# Sidebar for Explorer Profile
with st.sidebar:
    st.title("🚀 Mission Control")
    if 'explorer_name' not in st.session_state:
        st.session_state.explorer_name = st.text_input("Enter Explorer Name:", "Space Pioneer")
    
    st.subheader("Mission Stats")
    if 'missions_completed' not in st.session_state:
        st.session_state.missions_completed = 0
    
    st.metric("Missions Launched", st.session_state.missions_completed)
    
    # Achievement ranks
    st.subheader("Explorer Rank")
    ranks = {
        5: "🛸 Cosmic Rookie",
        10: "✨ Star Navigator",
        20: "🌌 Galaxy Pioneer",
        30: "⭐ Universal Master"
    }
    
    current_rank = max([level for level in ranks.keys() 
                       if st.session_state.missions_completed >= level] or [0])
    
    if current_rank > 0:
        st.markdown(f"<div class='achievement-badge'>{ranks[current_rank]}</div>", 
                   unsafe_allow_html=True)

# Main Mission Control
st.title("🚀 Growth Mindset Explorer")
st.write(f"Welcome, Explorer {st.session_state.explorer_name}! Ready for your next mission?")

# Mission Planning
with st.container():
    st.header("🎯 Launch New Mission")
    mission = st.text_area("What's your next growth mission?", 
                          placeholder="Example: Master the art of public speaking...")
    
    if st.button("Initialize Mission Plan"):
        if mission:
            with st.spinner("Calculating mission parameters..."):
                # Get AI responses
                refined_mission = query_huggingface({"inputs": f"Refine this growth mission: {mission}"})
                strategy = query_huggingface({"inputs": f"Create a 30-day strategy for: {mission}"})
                cosmic_wisdom = query_huggingface({"inputs": "Share cosmic wisdom about growth and exploration"})
                
                # Display mission briefing
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("<div class='mission-card'>", unsafe_allow_html=True)
                    st.subheader("🎯 Mission Objectives")
                    st.write(refined_mission)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div class='mission-card'>", unsafe_allow_html=True)
                    st.subheader("📅 30-Day Flight Plan")
                    st.write(strategy)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='quote-box'>", unsafe_allow_html=True)
                st.write(f"💫 *{cosmic_wisdom}*")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.session_state.missions_completed += 1
        else:
            st.warning("Please define your mission objectives!")

# Mission Progress Tracking
if 'mission_progress' not in st.session_state:
    st.session_state.mission_progress = [False] * 30

st.header("📊 Mission Progress")

# Create an interactive space journey tracker
progress_cols = st.columns(10)
for i in range(30):
    col_index = i % 10
    with progress_cols[col_index]:
        milestone_class = "progress-milestone milestone-active" if st.session_state.mission_progress[i] else "progress-milestone"
        st.markdown(f"<div class='{milestone_class}'>", unsafe_allow_html=True)
        day_complete = st.checkbox(f"D{i+1}", value=st.session_state.mission_progress[i], key=f"day_{i}")
        st.markdown("</div>", unsafe_allow_html=True)
        if day_complete != st.session_state.mission_progress[i]:
            st.session_state.mission_progress[i] = day_complete
            st.rerun()

# Progress visualization
completed = sum(st.session_state.mission_progress)
progress_percentage = (completed / 30) * 100

st.progress(progress_percentage / 100)
st.write(f"🌟 Mission Progress: {completed}/30 milestones achieved! ({progress_percentage:.1f}%)")

# Mission Status
if progress_percentage == 100:
    st.balloons()
    st.success("🌟 Mission Accomplished! You've reached all milestones!")
elif progress_percentage >= 75:
    st.info("🚀 Final approach initiated! Keep pushing forward!")
elif progress_percentage >= 50:
    st.info("💫 Halfway through your journey! Stay on course!")
elif progress_percentage >= 25:
    st.info("✨ Liftoff successful! Maintain trajectory!")
else:
    st.info("🛸 Pre-launch sequence initiated! Ready for takeoff!")

# Cosmic Tips
st.header("💫 Cosmic Wisdom")
cosmic_tips = [
    "The universe rewards those who dare to grow.",
    "Every challenge is a new star to reach for.",
    "Your potential is as limitless as space itself.",
    "Navigate through difficulties like a skilled astronaut.",
    "Each small step contributes to your cosmic journey.",
    "Embrace the unknown - that's where growth happens.",
    "Your mindset is your spacecraft through challenges.",
    "Chart your own course among the stars.",
    "Learn from every meteor and milestone.",
    "Your growth journey is writing constellations in the sky."
]
st.info(random.choice(cosmic_tips))

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: rgba(255,255,255,0.7);'>"
    "Exploring the infinite possibilities of growth 🌌"
    "</div>", 
    unsafe_allow_html=True
)
