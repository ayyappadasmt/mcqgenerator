import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables (API Key)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Choose a model
MODEL_NAME = "gemini-1.5-flash"

# Function to generate MCQs
def generate_mcqs(topic):
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = f"""
    Generate 5 multiple-choice questions (MCQs) about {topic}.
    Each question should have 4 answer choices (A, B, C, D), with the correct answer indicated.
    Provide the output in the following format:

    Q1. [Question]
    A) Option 1
    B) Option 2
    C) Option 3
    D) Option 4
    Answer: [Correct Option]
    """
    
    response = model.generate_content(prompt)
    return response.text

# Initialize session state
if "mcqs" not in st.session_state:
    st.session_state.mcqs = None
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = set()

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #F5F5DC;
        }
        .mcq-box {
            background-color: #EEE8AA;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 0px 8px #800080;
            margin: 10px 0;
        }
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #800080;
            text-align: center;
        }
        .question {
            font-size: 18px;
            font-weight: bold;
            color: #800080;
            text-align: center;
        }
        .answer {
            font-size: 16px;
            font-weight: bold;
            color: black;
            margin-top: 10px;
            text-align: center;
        }
        .score {
            font-size: 20px;
            font-weight: bold;
            color: #800080;
            text-align: center;
            margin-top: 20px;
        }
        .stButton > button {
            background-color: #800080 !important;
            color: white !important;
            font-size: 16px;
            padding: 10px;
            transition: 0.3s ease-in-out;
        }
        .stButton > button:hover {
            background-color: white !important;
            color: #800080 !important;
            border: 2px solid #800080;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.markdown("<h1 class='title'>0labs - AI-Powered MCQ Generator</h1>", unsafe_allow_html=True)

# Input field for topic
topic = st.text_input("Enter a topic for MCQs:")

if st.button("⚡ Generate MCQs"):
    if topic:
        with st.spinner("⏳ Generating MCQs..."):
            mcqs_text = generate_mcqs(topic)
            st.session_state.mcqs = mcqs_text.strip().split("\n\n")
            st.session_state.answers = {}
            st.session_state.score = 0
            st.session_state.answered = set()
    else:
        st.warning("⚠️ Please enter a topic!")

# Show MCQs if they exist
if st.session_state.mcqs:
    for i, mcq in enumerate(st.session_state.mcqs):
        parts = mcq.split("\n")
        if len(parts) >= 6:
            question = parts[0]
            options = parts[1:5]
            correct_answer = parts[5].replace("Answer: ", "").strip()

            st.markdown(f"<div class='mcq-box'>", unsafe_allow_html=True)
            st.markdown(f"<p class='question'>{question}</p>", unsafe_allow_html=True)

            selected_option = st.radio(f"Choose an answer:", options, index=None, key=f"q_{i}")

            if selected_option and i not in st.session_state.answered:
                st.session_state.answers[i] = selected_option
                st.session_state.answered.add(i)

                if selected_option.startswith(correct_answer):
                    st.session_state.score += 1

            if i in st.session_state.answered:
                if st.session_state.answers[i].startswith(correct_answer):
                    st.markdown(f"<p class='answer' style='color: #00ff00;'>✅ Correct! Answer: {correct_answer}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p class='answer' style='color: red;'>❌ Incorrect! Correct Answer: {correct_answer}</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # Display Score
    st.markdown(f"<p class='score'>🎯 Your Score: {st.session_state.score} / {len(st.session_state.mcqs)}</p>", unsafe_allow_html=True)
