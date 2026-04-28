import streamlit as st
import pandas as pd
import base64
import time
import random
import io
from pdfminer.high_level import extract_text
from streamlit_tags import st_tags
from PIL import Image
import nltk

# Download once safely
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords')

st.set_page_config(page_title="AI Resume Analyzer")

# -------- PDF Reader --------
def pdf_reader(file):
    return extract_text(file)

# -------- Show PDF --------
def show_pdf(file):
    file.seek(0)  # important fix
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# -------- Skill Extraction --------
def extract_skills(text):
    skills_db = [
        'python','java','c++','machine learning','deep learning',
        'flask','django','react','node js','sql','html','css',
        'javascript','data analysis','pandas','numpy'
    ]
    found = []
    for skill in skills_db:
        if skill.lower() in text.lower():
            found.append(skill)
    return list(set(found))

# -------- Main App --------
def run():
    st.title("📄 AI Resume Analyzer")

    pdf_file = st.file_uploader("Upload Resume", type=["pdf"])

    if pdf_file is not None:
        st.success("File uploaded successfully")

        # Show PDF
        show_pdf(pdf_file)

        # Save temporarily
        with open("temp.pdf", "wb") as f:
            f.write(pdf_file.getbuffer())

        with st.spinner("Analyzing Resume..."):
            time.sleep(2)

        # Extract text
        resume_text = pdf_reader("temp.pdf")

        # Extract skills
        skills = extract_skills(resume_text)

        st.subheader("🧠 Extracted Skills")
        st_tags(label='Skills', value=skills, key='1')

        # Experience level
        st.subheader("📊 Experience Level")
        if "intern" in resume_text.lower():
            st.success("Intermediate Level")
        elif "experience" in resume_text.lower():
            st.success("Experienced")
        else:
            st.warning("Fresher")

        # Resume Score
        score = 0
        if "project" in resume_text.lower():
            score += 25
        if "skill" in resume_text.lower():
            score += 25
        if "education" in resume_text.lower():
            score += 25
        if "experience" in resume_text.lower():
            score += 25

        st.subheader("📈 Resume Score")
        st.progress(score)
        st.write(f"Score: {score}/100")

        st.balloons()

# Run App
run()