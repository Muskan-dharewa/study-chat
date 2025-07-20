import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="Study Group Matcher", layout="wide")

# Background and styling
st.markdown(
    """
    <style>
    body {
        background-image: url('back.jpg');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
        padding: 2rem;
    }
    input, textarea, select {
        background-color: rgba(0,0,0,0.8) !important;
        color: white !important;
        border: 1px solid #888;
    }
    .css-1cpxqw2 {
        background-color: #A75D83 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📚 Study Group Matcher")
st.subheader("Match with students based on subjects, topics, goals, and timelines")

# ---- Form ----
with st.form("student_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    subject = st.selectbox("Subject", ["Math", "Physics", "Chemistry", "Biology", "History", "Computer Science", "Geography", "Civics"])
    topic = st.text_input("Topic (e.g., Calculus, Thermodynamics)")
    goal = st.text_area("Study Goal", placeholder="e.g., Revise formulas, solve 10 problems/day")
    exam_date = st.date_input("Exam Date")
    submit = st.form_submit_button("Find Study Group")

# ---- Database Simulation ----
if "students" not in st.session_state:
    st.session_state.students = []

# ---- Matchmaking Logic ----
if submit:
    if not name or not email or not topic or not goal:
        st.error("🚫 Please fill all the fields before submitting.")
    else:
        student = {
            "Name": name,
            "Email": email,
            "Subject": subject,
            "Topic": topic.lower(),
            "Goal": goal,
            "Exam Date": exam_date,
            "Timestamp": datetime.now()
        }
        st.session_state.students.append(student)

        # Match logic
        matches = [
            s for s in st.session_state.students
            if s["Subject"] == subject and s["Topic"] == topic.lower() and s["Email"] != email
        ]

        st.success(f"🎉 Welcome {name}! You've been added.")
        if matches:
            st.subheader("🎯 Matched Study Group Members")
            match_df = pd.DataFrame(matches)
            st.dataframe(match_df[["Name", "Email", "Goal", "Exam Date"]])
        else:
            st.info("No match found yet. You’ll be grouped once others register with similar interests.")

# ---- All Students Overview ----
st.divider()
st.subheader("📋 All Registered Students")
if st.session_state.students:
    all_df = pd.DataFrame(st.session_state.students)
    st.dataframe(all_df[["Name", "Subject", "Topic", "Goal", "Exam Date"]])
else:
    st.write("No students have registered yet.")

# ---- QUIZ BANK ----
QUIZ_BANK = {
    "Math": [
        ("What is the derivative of x^2?", "2x"),
        ("What is the integral of 1/x?", "ln|x|"),
        ("What is the value of sin(90°)?", "1"),
        ("What is 7 + 6 * 2?", "19"),
        ("What is the square root of 144?", "12"),
        ("What is 3 factorial (3!)?", "6"),
        ("What is the area of a circle with radius r?", "πr²"),
        ("What is the formula for slope?", "(y2 - y1)/(x2 - x1)"),
        ("If f(x) = 2x+3, what is f(2)?", "7"),
        ("What is the value of log(100) base 10?", "2")
    ],
    "Physics": [
        ("What is the unit of force?", "Newton"),
        ("Speed = ?", "Distance/Time"),
        ("What is the acceleration due to gravity?", "9.8"),
        ("What is Newton’s 2nd law?", "F=ma"),
        ("What does a volt measure?", "Electric potential"),
        ("SI unit of power?", "Watt"),
        ("Ohm's law formula?", "V=IR"),
        ("Which energy is stored in batteries?", "Chemical"),
        ("Current flows from?", "Positive to negative"),
        ("Lens used in magnifying glass?", "Convex")
    ],
    "Chemistry": [
        ("H2O is?", "Water"),
        ("Atomic number of Carbon?", "6"),
        ("pH < 7 means?", "Acidic"),
        ("What is NaCl?", "Salt"),
        ("Chemical formula of Methane?", "CH4"),
        ("Which gas is in soda?", "CO2"),
        ("Litmus turns red in?", "Acid"),
        ("Most reactive metal?", "Potassium"),
        ("Noble gases are in which group?", "18"),
        ("Boiling point of water?", "100")
    ],
    "Biology": [
        ("Basic unit of life?", "Cell"),
        ("Plants make food by?", "Photosynthesis"),
        ("DNA full form?", "Deoxyribonucleic Acid"),
        ("Heart has how many chambers?", "4"),
        ("Largest organ in body?", "Skin"),
        ("Gas used in respiration?", "Oxygen"),
        ("Which blood cells fight infection?", "White blood cells"),
        ("Which vitamin from sunlight?", "Vitamin D"),
        ("Blood is pumped by?", "Heart"),
        ("Organ for breathing?", "Lungs")
    ],
    "History": [
        ("Who was first President of India?", "Rajendra Prasad"),
        ("Father of Indian Constitution?", "B.R. Ambedkar"),
        ("When did WW2 end?", "1945"),
        ("Who discovered America?", "Christopher Columbus"),
        ("Mughal emperor during 1857?", "Bahadur Shah Zafar"),
        ("Who led Dandi March?", "Mahatma Gandhi"),
        ("Capital of Mauryan Empire?", "Pataliputra"),
        ("Battle of Plassey year?", "1757"),
        ("Who built Red Fort?", "Shah Jahan"),
        ("Quit India Movement year?", "1942")
    ],
    "Computer Science": [
        ("Full form of CPU?", "Central Processing Unit"),
        ("Binary of 5?", "101"),
        ("What does HTML stand for?", "HyperText Markup Language"),
        ("RAM stands for?", "Random Access Memory"),
        ("Python is a?", "Programming Language"),
        ("1 byte = ?", "8 bits"),
        ("Shortcut to copy?", "Ctrl+C"),
        ("Loop that never ends?", "Infinite Loop"),
        ("What is AI?", "Artificial Intelligence"),
        ("What is an algorithm?", "Step-by-step procedure")
    ],
    "Geography": [
        ("Largest continent?", "Asia"),
        ("River that flows through Egypt?", "Nile"),
        ("Earth shape?", "Geoid"),
        ("Tallest mountain?", "Mount Everest"),
        ("Which layer has ozone?", "Stratosphere"),
        ("Rain gauge measures?", "Rainfall"),
        ("Capital of France?", "Paris"),
        ("Hottest desert?", "Sahara"),
        ("Which ocean is largest?", "Pacific"),
        ("Seasons caused by?", "Earth’s tilt")
    ]
}

# ---- QUIZ SECTION ----
st.divider()
st.subheader("🧠 Practice Quiz")

selected_subject = st.selectbox("Select subject for quiz", list(QUIZ_BANK.keys()), key="quiz_subject")
if st.button("Start Quiz"):
    quiz = random.sample(QUIZ_BANK[selected_subject], 10)
    for idx, (question, answer) in enumerate(quiz, 1):
        st.markdown(f"**Q{idx}. {question}**")
        with st.expander("Show Answer"):
            st.write(f"✅ **{answer}**")
