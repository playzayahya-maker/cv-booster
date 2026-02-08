import streamlit as st
from groq import Groq
from fpdf import FPDF
import re

# --- UI Setup ---
st.set_page_config(page_title="UNIVERSAL ATS ARCHITECT", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #fff; }
    .main-header { color: #00FF9D; text-align: center; font-size: 35px; font-weight: 800; }
    .paper-box { background: white; color: #1e293b; padding: 40px; border-radius: 5px; font-family: 'Times', serif; }
</style>
""", unsafe_allow_html=True)

# --- PDF Engine ---
def create_pro_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=11)
    clean_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    pdf.multi_cell(0, 8, clean_text)
    return pdf.output()

st.markdown("<h1 class='main-header'>UNIVERSAL ATS ARCHITECT PRO</h1>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🔐 ACCESS")
    api_key = st.text_input("Enter Groq Key:", type="password")
    style = st.selectbox("Style Target:", ["CANADA (Strict)", "USA (Modern)", "EUROPE (Standard)"])

# --- Input Area ---
st.markdown("### 👤 PASTE YOUR BACKGROUND / OLD CV")
user_input = st.text_area("Hna lo7 ghir l-m3loumat dyalk (Experience, Skills, Study...):", height=300)

if st.button("GENERATE MASTER ATS PACKAGE ⚡", use_container_width=True):
    if not api_key:
        st.error("API Key missing!")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner("🧠 Architecting an All-Purpose Professional CV..."):
                
                # Prompt i7tirafi: makay-7tajch Job Description
                prompt = f"""
                You are a Master Career Consultant for {style} markets.
                Target: Create a 'Master CV' and 'Generic but High-Impact Cover Letter' that passes any ATS.
                
                Input Data: {user_input}
                
                Instructions:
                1. Professional Formatting: No photos/age for Canada/USA.
                2. STAR Method: Rewrite every experience point to show results and numbers.
                3. Industry Keywords: Use the most standard high-value keywords for this user's specific field.
                4. Tone: Persuasive, confident, and elite.
                
                Structure: 
                - CV Section (Title it clearly)
                - Cover Letter Section (General but powerful)
                """
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )
                st.session_state['output'] = res.choices[0].message.content
        except Exception as e:
            st.error(f"Error: {e}")

# --- Results ---
if 'output' in st.session_state:
    st.markdown("<div class='paper-box'>", unsafe_allow_html=True)
    st.markdown(st.session_state['output'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    pdf_file = create_pro_pdf(st.session_state['output'])
    st.download_button("📥 DOWNLOAD MASTER PDF", data=pdf_file, file_name="Master_ATS_Package.pdf", mime="application/pdf")
