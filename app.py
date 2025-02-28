import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate quiz
def generate_quiz(topic):
    prompt = f"Generate 5 multiple-choice questions about {topic} with 4 answer choices each."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change model
        messages=[
            {"role": "system", "content": "You are a quiz generator."},
            {"role": "user", "content": "Generate 5 MCQs on Newton's Laws of Motion."}
        ]
    )
    
    return response["choices"][0]["message"]["content"]

# Custom CSS for neon theme
st.markdown(
    """
    <style>
    body {
        background-color: #0d0d0d;
        color: #ff66cc;
        font-family: 'Courier New', monospace;
    }
    .stTextInput > div > div > input {
        background-color: black;
        color: #00ccff;
        border: 2px solid #ff66cc;
        padding: 10px;
        font-size: 18px;
        transition: all 0.3s ease-in-out;
    }
    .stTextInput > div > div > input:focus {
        border: 2px solid #00ccff;
        box-shadow: 0 0 10px #ff66cc, 0 0 20px #00ccff;
    }
    .stButton > button {
        background-color: #ff66cc;
        color: black;
        font-size: 18px;
        font-weight: bold;
        padding: 12px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #00ccff;
        color: white;
        box-shadow: 0 0 15px #ff66cc, 0 0 25px #00ccff;
        transform: scale(1.05);
    }
    .title {
        font-size: 40px;
        text-align: center;
        text-shadow: 0 0 10px #ff66cc, 0 0 20px #00ccff;
        animation: glow 1.5s infinite alternate;
    }
    @keyframes glow {
        from {
            text-shadow: 0 0 10px #ff66cc, 0 0 20px #00ccff;
        }
        to {
            text-shadow: 0 0 15px #ff66cc, 0 0 25px #00ccff;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("0lAbs")
st.markdown('<h1 class="title"> AI MCQ Quiz Generator</h1>', unsafe_allow_html=True)

topic = st.text_input("🎓 Enter Experiment Topic:")

if st.button("Generate Quiz"):
    with st.spinner(" Generating MCQs..."):
        quiz = generate_quiz(topic)
    st.markdown("##  MCQs:")
    st.write(quiz)


