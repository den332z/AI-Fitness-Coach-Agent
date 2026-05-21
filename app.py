import streamlit as st
from openai import OpenAI
import os
import requests
from dotenv import load_dotenv

# Load your API_NINJAS_KEY from the .env file
load_dotenv()

# Connect to your local LM Studio server
client = OpenAI(
    base_url="http://localhost:1234/v1", 
    api_key="lm-studio"
)

# --- Tool: API Ninjas Exercise Fetcher + Anatomy Visualizer ---
def fetch_exercises(muscle):
    api_url = f'https://api.api-ninjas.com/v1/exercises?muscle={muscle}'
    api_key = os.environ.get("API_NINJAS_KEY")
    
    m = muscle.lower().strip()
    
    # 1. Visual Anatomy Diagram UI
    st.markdown(f"### 📊 Anatomy Breakdown: {muscle.title()}")
    
    # Changed columns to [1, 3] to make the image smaller and text wider
    if m == "chest":
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("Parts/Chest.png", caption="Pectoralis Major", use_container_width=True)
        with col2:
            st.markdown("""
            * **Upper Chest:** Targeted via incline movements.
            * **Middle Chest:** Targeted via flat pressing movements.
            * **Lower Chest:** Targeted via decline movements or dips.
            """)
            
    elif m == "back":
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("Parts/Back.png", caption="Posterior Chain", use_container_width=True)
        with col2:
            st.markdown("""
            * **Latissimus Dorsi:** Responsible for back width.
            * **Trapezius & Rhomboids:** Responsible for thickness.
            * **Erector Spinae:** Structural stability (deadlifts).
            """)
            
    elif m in ["biceps", "bicep"]:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("Parts/Bicep.png", caption="Biceps Brachii", use_container_width=True)
        with col2:
            st.markdown("""
            * **Long Head:** Creates the "peak" (Incline Curls).
            * **Short Head:** Adds width (Preacher Curls).
            * **Brachialis:** Pushes bicep up (Hammer Curls).
            """)
            
    elif m in ["triceps", "tricep"]:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("Parts/Triceps.png", caption="Triceps Brachii", use_container_width=True)
        with col2:
            st.markdown("""
            * **Long Head:** Targeted with overhead extensions.
            * **Lateral Head:** The outer "horseshoe" (pushdowns).
            * **Medial Head:** Deep stabilizing muscle.
            """)
            
    elif m in ["shoulders", "shoulder", "delts"]:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("Parts/Shoulders.png", caption="Deltoids", use_container_width=True)
        with col2:
            st.markdown("""
            * **Anterior Delt:** Pushing and front raises.
            * **Lateral Delt:** Creates shoulder width.
            * **Posterior Delt:** Posture and pulling.
            """)
            
    elif m in ["quads", "quadriceps"]:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("Parts/Quads.png", caption="Quadriceps", use_container_width=True)
        with col2:
            st.markdown("""
            * **Rectus Femoris:** Crosses the hip.
            * **Vastus Lateralis:** Outer thigh sweep.
            * **Vastus Medialis:** The "teardrop".
            """)
            
    elif m in ["hamstrings", "calves", "hams", "legs"]:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("Parts/Hams_Calves.png", caption="Posterior Leg", use_container_width=True)
        with col2:
            st.markdown("""
            * **Hamstrings:** Knee flexion and hip extension.
            * **Gastrocnemius:** Main calf muscle.
            * **Soleus:** Deep calf muscle.
            """)
            
    elif m in ["abs", "abdominals", "core"]:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("Parts/Abs.png", caption="Abdominal Wall", use_container_width=True)
        with col2:
            st.markdown("""
            * **Rectus Abdominis:** The "six-pack".
            * **Obliques:** Rotation and lateral flexion.
            * **Transverse Abdominis:** Deep core stabilizer.
            """)
            
    else:
        st.caption(f"*(Visual anatomy diagram for {muscle} not currently loaded.)*")

    st.markdown("---") 

    # 2. Proceed with API Data Fetching
    try:
        response = requests.get(api_url, headers={'X-Api-Key': api_key})
        if response.status_code == requests.codes.ok:
            data = response.json()
            if not data:
                return f"No verified exercises found for '{muscle}' in the database."
            exercises = [ex['name'] for ex in data[:3]]
            return f"Verified {muscle} exercises from database: " + ", ".join(exercises)
        else:
            return "Exercise API currently unavailable."
    except Exception:
        return "Exercise API connection failed."

# --- Page Configuration ---
st.set_page_config(page_title="AI Fitness Coach", page_icon="🏋️", layout="wide")

# --- UI: Sidebar Settings ---
with st.sidebar:
    st.title("⚙️ Dashboard")
    st.markdown("---")
    
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.caption("Agent Status: **Online**")
    st.caption("Local Engine: **Llama 3 (8B)**")
    st.caption("Tool API: **API Ninjas**")

# --- System Prompt & Memory ---
SYSTEM_PROMPT = """You are an expert AI Personal Fitness Coach. 

### CORE PROTOCOLS:
1. ALWAYS ask for goals, schedule, and equipment before generating any plan.
2. Think step-by-step before answering. Format plans with bold headers and bullet points.
3. TOOL TRIGGER (CRITICAL): If the user asks for exercises for ANY specific muscle group (e.g., back, chest, legs, shoulders, biceps, abs), you MUST stop generating and ONLY reply with the exact format [FETCH: muscle_name]. Do not write any other text! Example: If they ask for back, reply ONLY with [FETCH: back].

### SAFETY & SCOPE GUARDRAILS:
4. INJURY PREVENTION: Never recommend exercises for injured areas without noting proper form and advising a consult with a professional.
5. NUTRITION LIMITATION: You are a fitness coach, NOT a dietitian. For nutrition questions, provide general macro guidance only and ALWAYS include a disclaimer.
6. ADVANCED PROGRAMMING: For high-intensity or powerlifting requests, provide a template but add a disclaimer that advanced programs should be monitored by a human coach.
7. OFF-TOPIC RULE: Politely decline and redirect any non-fitness related questions back to the user's fitness journey.

Introduce yourself as an AI Coach, not a medical professional."""

if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- UI: Main Chat Interface ---
st.title("🦾 AI Personal Fitness Coach")
st.markdown("Your adaptive, intelligent training partner. Log your workout or ask for a new split.")
st.divider()

USER_AVATAR = "👤"
COACH_AVATAR = "🏋️‍♂️"

for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = USER_AVATAR if message["role"] == "user" else COACH_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

if len(st.session_state.messages) == 1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**New Plan**\n\n'I want to build muscle, 4 days a week, gym access.'")
    with col2:
        st.info("**Log Workout**\n\n'I just finished 4 sets of heavy deadlifts.'")
    with col3:
        st.info("**Form Check**\n\n'What are some good exercises for my chest?'")

# --- Chat Input & Dispatcher Logic ---
if prompt := st.chat_input("What are your fitness goals or what did you train today?"):
    
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar=COACH_AVATAR):
        with st.spinner("Analyzing parameters..."):
            stream = client.chat.completions.create(
                model="local-model",
                messages=st.session_state.messages,
                stream=False, 
            )
            
            initial_response = stream.choices[0].message.content
        
        if "[FETCH:" in initial_response:
            start = initial_response.find("[FETCH:") + 7
            end = initial_response.find("]", start)
            muscle = initial_response[start:end].strip().lower()
            
            st.toast(f"Fetching real exercises for: {muscle}...", icon="🔍")
            
            # This triggers the API and prints your Anatomy UI!
            api_data = fetch_exercises(muscle)
            
            temp_messages = st.session_state.messages.copy()
            temp_messages.append({"role": "assistant", "content": initial_response})
            
            follow_up_instruction = (
                f"Data fetched: {api_data}\n\n"
                "Act as my coach and provide this list to me now. "
                "STRICT RULES: \n"
                "1. DO NOT apologize or mention this data fetch. Start your response directly with an encouraging coach phrase (e.g., 'Here are some great exercises to target...').\n"
                "2. Format as a clean Markdown list. You MUST use a double line break (press Enter twice) after every single exercise so they do not bunch up into one paragraph.\n"
                "3. Include a form tip and the YouTube link EXACTLY like this for each: [🎥 Watch Tutorial](https://www.youtube.com/results?search_query=Exact+Exercise+Name+form+tutorial)."
            )
            temp_messages.append({"role": "user", "content": follow_up_instruction})
            
            final_stream = client.chat.completions.create(
                model="local-model",
                messages=temp_messages, # We send the temporary memory here!
                stream=True,
            )
            final_response = st.write_stream(final_stream)
            
            # We ONLY save the final, clean response to the permanent chat history
            st.session_state.messages.append({"role": "assistant", "content": final_response})
            
        else:
            st.markdown(initial_response)
            st.session_state.messages.append({"role": "assistant", "content": initial_response})