import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv()  
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

input_prompt = """
Hey Act like a skilled or very experience ATS(Application Tracking System) with the deep understanding of 
tech field , software engineering, data science, data analyst and Big data engineer. Your task is to evaluate the
resume based on the given job description. You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage matching based on JD and the missing keywords with high 
accuracy 
resume : {text}
description : {JD}

I want the response in one single string having the structure 
{{"JD Match" : "%", "Missing Keywords : []", "Profile Summary": ""}}
"""

st.title("ResumeGenie")
st.text("Improve your resume ATS")
jd = st.text_area("Enter the Job Description or the Role")
uploaded_file = st.file_uploader("Upload your Resume", type="pdf", help="Please upload the PDF")
submit = st.button("Submit")

# Initialize cached response using session_state
if 'cached_response' not in st.session_state:
    st.session_state.cached_response = None

# Store JD and resume details in separate variables
if 'cached_jd' not in st.session_state:
    st.session_state.cached_jd = ""
if 'cached_resume_text' not in st.session_state:
    st.session_state.cached_resume_text = ""

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)

        # Check if JD or resume text has changed
        if jd != st.session_state.cached_jd or text != st.session_state.cached_resume_text:
            input_prompt_with_text = input_prompt.format(text=text, JD=jd)
            response = get_gemini_response(input_prompt_with_text)
            st.subheader(response)
            st.session_state.cached_response = response
            st.session_state.cached_jd = jd
            st.session_state.cached_resume_text = text
        else:
            # Use cached response
            st.subheader(st.session_state.cached_response)