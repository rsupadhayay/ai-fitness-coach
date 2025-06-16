import streamlit as st
import streamlit.components.v1 as components
# import openai  # Commented out for now
from typing import Dict, List
import json
import random

# Page configuration
st.set_page_config(
    page_title="AI Fitness Coach - Kartik",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client (when available)
@st.cache_resource
def init_openai():
    try:
        import openai
        return openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    except ImportError:
        return None

# Exercise database with video demonstrations
EXERCISES_DB = {
    "Chest": {
        "Push-ups": {
            "description": "Classic bodyweight exercise targeting chest, shoulders, and triceps",
            "instructions": "Start in plank position, lower chest to ground, push back up",
            "sets_reps": "3 sets of 10-15 reps",
            "difficulty": "Beginner",
            "equipment": "None",
            "video_url": "https://www.youtube.com/watch?v=IODxDxX7oi4",
            "video_embed": "https://www.youtube.com/embed/IODxDxX7oi4"
        },
        "Bench Press": {
            "description": "Premier chest building exercise using barbell or dumbbells",
            "instructions": "Lie on bench, lower weight to chest, press up explosively",
            "sets_reps": "4 sets of 8-12 reps",
            "difficulty": "Intermediate",
            "equipment": "Barbell/Dumbbells, Bench",
            "video_url": "https://www.youtube.com/watch?v=rT7DgCr-3pg",
            "video_embed": "https://www.youtube.com/embed/rT7DgCr-3pg"
        },
        "Chest Dips": {
            "description": "Bodyweight exercise focusing on lower chest development",
            "instructions": "Support body on parallel bars, lower until stretch, push back up",
            "sets_reps": "3 sets of 8-12 reps",
            "difficulty": "Intermediate",
            "equipment": "Dip bars",
            "video_url": "https://www.youtube.com/watch?v=2z8JmcrW-As",
            "video_embed": "https://www.youtube.com/embed/2z8JmcrW-As"
        }
    },
    "Back": {
        "Pull-ups": {
            "description": "Ultimate upper body pulling exercise for back and biceps",
            "instructions": "Hang from bar, pull chest to bar, lower with control",
            "sets_reps": "3 sets of 5-10 reps",
            "difficulty": "Intermediate",
            "equipment": "Pull-up bar",
            "video_url": "https://www.youtube.com/watch?v=eGo4IYlbE5g",
            "video_embed": "https://www.youtube.com/embed/eGo4IYlbE5g"
        },
        "Deadlifts": {
            "description": "King of all exercises, targets entire posterior chain",
            "instructions": "Lift barbell from ground to hip level, maintain straight back",
            "sets_reps": "4 sets of 5-8 reps",
            "difficulty": "Advanced",
            "equipment": "Barbell, Plates",
            "video_url": "https://www.youtube.com/watch?v=op9kVnSso6Q",
            "video_embed": "https://www.youtube.com/embed/op9kVnSso6Q"
        },
        "Bent-over Rows": {
            "description": "Excellent for building thick, wide back muscles",
            "instructions": "Bend at hips, pull weight to lower chest, squeeze shoulder blades",
            "sets_reps": "4 sets of 8-12 reps",
            "difficulty": "Intermediate",
            "equipment": "Barbell/Dumbbells",
            "video_url": "https://www.youtube.com/watch?v=FWJR5Ve8bnQ",
            "video_embed": "https://www.youtube.com/embed/FWJR5Ve8bnQ"
        }
    },
    "Legs": {
        "Squats": {
            "description": "King of leg exercises, targets quads, glutes, and hamstrings",
            "instructions": "Lower hips back and down, keep chest up, drive through heels",
            "sets_reps": "4 sets of 10-15 reps",
            "difficulty": "Beginner",
            "equipment": "None/Barbell",
            "video_url": "https://www.youtube.com/watch?v=Dy28eq2PjcM",
            "video_embed": "https://www.youtube.com/embed/Dy28eq2PjcM"
        },
        "Lunges": {
            "description": "Unilateral leg exercise improving balance and strength",
            "instructions": "Step forward, lower back knee toward ground, return to start",
            "sets_reps": "3 sets of 12 reps each leg",
            "difficulty": "Beginner",
            "equipment": "None/Dumbbells",
            "video_url": "https://www.youtube.com/watch?v=QOVaHwm-Q6U",
            "video_embed": "https://www.youtube.com/embed/QOVaHwm-Q6U"
        },
        "Romanian Deadlifts": {
            "description": "Targets hamstrings and glutes with hip hinge movement",
            "instructions": "Push hips back, lower weight along legs, feel hamstring stretch",
            "sets_reps": "3 sets of 10-12 reps",
            "difficulty": "Intermediate",
            "equipment": "Barbell/Dumbbells",
            "video_url": "https://www.youtube.com/watch?v=2SHsk9AzdjA",
            "video_embed": "https://www.youtube.com/embed/2SHsk9AzdjA"
        }
    },
    "Shoulders": {
        "Overhead Press": {
            "description": "Primary shoulder building exercise for strength and mass",
            "instructions": "Press weight from shoulders overhead, keep core tight",
            "sets_reps": "4 sets of 8-10 reps",
            "difficulty": "Intermediate",
            "equipment": "Barbell/Dumbbells",
            "video_url": "https://www.youtube.com/watch?v=QAQ64hK4Xxs",
            "video_embed": "https://www.youtube.com/embed/QAQ64hK4Xxs"
        },
        "Lateral Raises": {
            "description": "Isolation exercise for side deltoids and shoulder width",
            "instructions": "Raise arms to sides until parallel to ground, control descent",
            "sets_reps": "3 sets of 12-15 reps",
            "difficulty": "Beginner",
            "equipment": "Dumbbells",
            "video_url": "https://www.youtube.com/watch?v=3VcKaXpzqRo",
            "video_embed": "https://www.youtube.com/embed/3VcKaXpzqRo"
        },
        "Pike Push-ups": {
            "description": "Bodyweight exercise targeting front deltoids",
            "instructions": "In downward dog position, lower head toward ground, push back up",
            "sets_reps": "3 sets of 8-12 reps",
            "difficulty": "Intermediate",
            "equipment": "None",
            "video_url": "https://www.youtube.com/watch?v=spoSDWI_Ny8",
            "video_embed": "https://www.youtube.com/embed/spoSDWI_Ny8"
        }
    },
    "Arms": {
        "Bicep Curls": {
            "description": "Classic bicep isolation exercise for arm development",
            "instructions": "Curl weight from extended position to chest, squeeze bicep",
            "sets_reps": "3 sets of 10-12 reps",
            "difficulty": "Beginner",
            "equipment": "Dumbbells/Barbell",
            "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
            "video_embed": "https://www.youtube.com/embed/ykJmrZ5v0Oo"
        },
        "Tricep Dips": {
            "description": "Bodyweight exercise targeting triceps for arm strength",
            "instructions": "Support on chair/bench, lower body, press back up",
            "sets_reps": "3 sets of 10-15 reps",
            "difficulty": "Beginner",
            "equipment": "Chair/Bench",
            "video_url": "https://www.youtube.com/watch?v=6kALZikXxLc",
            "video_embed": "https://www.youtube.com/embed/6kALZikXxLc"
        },
        "Close-grip Push-ups": {
            "description": "Push-up variation emphasizing triceps development",
            "instructions": "Hands close together, lower chest to hands, push up",
            "sets_reps": "3 sets of 8-12 reps",
            "difficulty": "Intermediate",
            "equipment": "None",
            "video_url": "https://www.youtube.com/watch?v=42luHhrsNhg",
            "video_embed": "https://www.youtube.com/embed/42luHhrsNhg"
        }
    },
    "Core": {
        "Plank": {
            "description": "Isometric core exercise for stability and strength",
            "instructions": "Hold straight line from head to heels, engage core",
            "sets_reps": "3 sets of 30-60 seconds",
            "difficulty": "Beginner",
            "equipment": "None",
            "video_url": "https://www.youtube.com/watch?v=ASdvN_XEl_c",
            "video_embed": "https://www.youtube.com/embed/ASdvN_XEl_c"
        },
        "Bicycle Crunches": {
            "description": "Dynamic core exercise targeting obliques and abs",
            "instructions": "Alternate bringing elbow to opposite knee in cycling motion",
            "sets_reps": "3 sets of 20 reps each side",
            "difficulty": "Beginner",
            "equipment": "None",
            "video_url": "https://www.youtube.com/watch?v=9FGilxCbdz8",
            "video_embed": "https://www.youtube.com/embed/9FGilxCbdz8"
        },
        "Russian Twists": {
            "description": "Rotational core exercise for oblique strength",
            "instructions": "Sit with feet off ground, rotate torso side to side",
            "sets_reps": "3 sets of 20 reps each side",
            "difficulty": "Intermediate",
            "equipment": "None/Medicine Ball",
            "video_url": "https://www.youtube.com/watch?v=wkD8rjkodUI",
            "video_embed": "https://www.youtube.com/embed/wkD8rjkodUI"
        }
    }
}

def get_ai_response(client, prompt: str, user_input: str) -> str:
    """Get response from AI trainer Kartik"""
    if client is None:
        return "Hi! I'm Kartik, your fitness trainer. OpenAI integration is currently unavailable, but I'd love to help you with your fitness journey! Try the exercise library below for detailed workout information."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are Kartik, an enthusiastic and knowledgeable AI fitness trainer. 
                    You are supportive, motivating, and provide expert fitness advice. 
                    Keep responses conversational, encouraging, and informative. 
                    Always focus on proper form, safety, and gradual progression.
                    Address the user directly and be personable.
                    
                    Context: {prompt}"""
                },
                {"role": "user", "content": user_input}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I'm having trouble connecting right now. Error: {str(e)}"

def main():
    # Header
    st.title("💪 AI Fitness Coach - Kartik")
    st.markdown("### Your Personal AI Fitness Trainer with Video Demonstrations")
    
    # Add a featured video section
    with st.container():
        st.markdown("### 🌟 Featured Exercise of the Day")
        featured_col1, featured_col2 = st.columns([1, 1])
        
        with featured_col1:
            st.markdown("**💥 Push-ups - Perfect for Everyone!**")
            featured_video_html = """
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
                <iframe src="https://www.youtube.com/embed/IODxDxX7oi4" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                        allowfullscreen>
                </iframe>
            </div>
            """
            st.components.v1.html(featured_video_html, height=200)
        
        with featured_col2:
            st.markdown("""
            **Why Push-ups?**
            - ✅ No equipment needed
            - ✅ Works multiple muscle groups  
            - ✅ Great for all fitness levels
            - ✅ Can be done anywhere
            
            Start with 3 sets of 5-10 reps and build up gradually!
            """)
        
        st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=400&fit=crop", 
                caption="Your AI Trainer - Kartik", width=250)
        st.markdown("---")
        st.markdown("**💬 Chat with Kartik**")
        st.markdown("Ask me anything about fitness, exercises, or workout plans!")

    # Main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Exercise Selection
        st.header("🎯 Exercise Library")
        
        # Body part selection
        selected_body_part = st.selectbox(
            "Choose a body part to train:",
            list(EXERCISES_DB.keys()),
            index=0
        )
        
        # Display exercises for selected body part
        st.subheader(f"{selected_body_part} Exercises")
        
        # Add a "View All Videos" toggle
        show_all_videos = st.toggle("📺 Show All Videos at Once", value=False)
        
        if show_all_videos:
            st.markdown("### 🎬 Video Gallery")
            # Create a grid of videos
            video_cols = st.columns(2)
            exercise_list = list(exercises.items())
            
            for idx, (exercise_name, exercise_data) in enumerate(exercise_list):
                with video_cols[idx % 2]:
                    st.markdown(f"**{exercise_name}**")
                    video_html = f"""
                    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; margin-bottom: 10px;">
                        <iframe src="{exercise_data['video_embed']}" 
                                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                                allowfullscreen>
                        </iframe>
                    </div>
                    """
                    st.components.v1.html(video_html, height=200)
            
            st.markdown("---")
        
        exercises = EXERCISES_DB[selected_body_part]
        
        for exercise_name, exercise_data in exercises.items():
            with st.expander(f"💪 {exercise_name} - {exercise_data['difficulty']}", expanded=False):
                # Create columns for video and details
                col_video, col_details = st.columns([1, 1])
                
                with col_video:
                    st.subheader("📹 Video Demonstration")
                    # Embed YouTube video
                    video_html = f"""
                    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
                        <iframe src="{exercise_data['video_embed']}" 
                                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                                allowfullscreen>
                        </iframe>
                    </div>
                    """
                    st.components.v1.html(video_html, height=250)
                    
                    # Link to full video
                    st.markdown(f"🔗 [Watch on YouTube]({exercise_data['video_url']})")
                
                with col_details:
                    st.subheader("📋 Exercise Details")
                    st.write(f"**Description:** {exercise_data['description']}")
                    st.write(f"**Instructions:** {exercise_data['instructions']}")
                    st.write(f"**Sets/Reps:** {exercise_data['sets_reps']}")
                    st.write(f"**Equipment:** {exercise_data['equipment']}")
                    st.write(f"**Difficulty:** {exercise_data['difficulty']}")
                    
                    # Get AI advice button
                    if st.button(f"Ask Kartik about {exercise_name}", key=f"ask_{exercise_name}"):
                        client = init_openai()
                        if client is not None and "OPENAI_API_KEY" in st.secrets:
                            prompt = f"The user is asking about the {exercise_name} exercise for {selected_body_part}. Exercise details: {exercise_data}"
                            question = f"Can you give me tips and advice about {exercise_name}?"
                            response = get_ai_response(client, prompt, question)
                            st.success(f"**Kartik says:** {response}")
                        else:
                            st.info("💡 **Exercise Tips:**\n\n" + 
                                   f"**{exercise_name}** is great for {selected_body_part.lower()}! " +
                                   "Focus on proper form, start with lighter weights, and gradually increase intensity. " +
                                   "Remember to breathe properly and maintain good posture throughout the movement.")
                            if client is None:
                                st.warning("Install openai package (`pip install openai`) to chat with AI trainer Kartik!")
                
                # Add a divider between exercises
                st.markdown("---")

    with col2:
        # AI Chat Interface
        st.header("💬 Chat with Kartik")
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Chat input
        user_question = st.text_area(
            "Ask Kartik anything about fitness:",
            placeholder="e.g., How do I build muscle? What's a good beginner workout? How to lose weight?",
            height=100
        )
        
        if st.button("Send to Kartik", type="primary"):
            if user_question:
                client = init_openai()
                
                if client is not None and "OPENAI_API_KEY" in st.secrets:
                    # Add context about current page
                    context = f"User is currently viewing exercises for {selected_body_part}. Available exercises: {list(exercises.keys())}"
                    
                    response = get_ai_response(client, context, user_question)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "user": user_question,
                        "kartik": response
                    })
                    
                    # Clear input
                    st.rerun()
                else:
                    # Provide basic responses without AI
                    basic_response = "Thanks for your question! While I'd love to give you personalized advice, my AI capabilities are currently limited. Check out the exercise library for detailed instructions on proper form and technique!"
                    
                    st.session_state.chat_history.append({
                        "user": user_question,
                        "kartik": basic_response
                    })
                    
                    if client is None:
                        st.warning("Install openai package to enable full AI chat features!")
                    else:
                        st.warning("Please add your OpenAI API key to Streamlit secrets!")
                    
                    st.rerun()
            else:
                st.warning("Please enter a question!")
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.subheader("Chat History")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5 chats
                with st.container():
                    st.markdown(f"**You:** {chat['user']}")
                    st.markdown(f"**Kartik:** {chat['kartik']}")
                    st.markdown("---")
        
        # Workout Tips
        st.markdown("---")
        st.subheader("🎯 Quick Workout Builder")
        
        # Workout builder
        if st.button("🏋️ Generate Quick Workout", type="secondary"):
            # Select random exercises from different body parts
            workout_exercises = []
            body_parts = ["Chest", "Back", "Legs", "Core"]
            
            for body_part in body_parts:
                available_exercises = list(EXERCISES_DB[body_part].keys())
                selected_exercise = random.choice(available_exercises)
                workout_exercises.append((body_part, selected_exercise, EXERCISES_DB[body_part][selected_exercise]))
            
            st.markdown("### 🔥 Your Custom Workout")
            for body_part, exercise_name, exercise_data in workout_exercises:
                with st.expander(f"💪 {exercise_name} ({body_part})", expanded=True):
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        video_html = f"""
                        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
                            <iframe src="{exercise_data['video_embed']}" 
                                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                                    allowfullscreen>
                            </iframe>
                        </div>
                        """
                        st.components.v1.html(video_html, height=150)
                    with col2:
                        st.write(f"**{exercise_data['sets_reps']}**")
                        st.write(f"*{exercise_data['description']}*")
        
        st.markdown("---")
        st.subheader("💡 Quick Tips from Kartik")
        tips = [
            "Always warm up before exercising",
            "Focus on proper form over heavy weights",
            "Stay hydrated throughout your workout",
            "Get adequate rest between workout days",
            "Listen to your body and avoid overtraining"
        ]
        
        for tip in tips:
            st.markdown(f"• {tip}")

    # Footer
    st.markdown("---")
    st.markdown("""
    **✨ NEW: Video Demonstrations Added!**
    - 📹 Watch proper form for every exercise
    - 🎬 Video gallery view for quick reference  
    - 🔗 Direct YouTube links for detailed tutorials
    
    **Setup Instructions:**
    1. Install Streamlit: `pip install streamlit`
    2. For AI features, install OpenAI: `pip install openai`
    3. Add your OpenAI API key to Streamlit secrets (optional)
    4. Run with: `streamlit run app.py`
    
    **Features:**
    - ✅ 18 exercises with HD video demonstrations
    - ✅ AI trainer Kartik for personalized advice
    - ✅ Exercise library with detailed instructions
    - ✅ Video gallery mode for quick browsing
    - ✅ Mobile-friendly responsive design
    
    **Note:** Videos are embedded from YouTube for the best quality demonstrations. 
    For full AI chat with Kartik, add your OpenAI API key in `.streamlit/secrets.toml`:
    ```
    OPENAI_API_KEY = "your-api-key-here"
    ```
    
    **Troubleshooting Architecture Issues (Apple Silicon Macs):**
    If you get pydantic_core errors, try:
    ```bash
    pip install --upgrade --force-reinstall --no-cache-dir streamlit openai
    ```
    """)

if __name__ == "__main__":
    main()