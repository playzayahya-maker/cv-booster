import streamlit as st
from groq import Groq
from fpdf import FPDF
import re

# --- UI CONFIG (Cyber Pro Style) ---
st.set_page_config(page_title="NEURAL ARCHITECT V13", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-header { color: #00FF9D; text-align: center; font-size: 35px; font-weight: 900; padding: 20px; border-bottom: 2px solid #1e293b; }
    .input-section { background: #0f172a; padding: 25px; border-radius: 15px; border: 1px solid #1e293b; min-height: 450px; }
    .paper { background: white; color: #1a1a1a; padding: 30px; border-radius: 4px; font-family: 'Times New Roman', serif; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }
    .stButton>button { background: #00FF9D; color: #000; font-weight: 800; border-radius: 8px; transition: 0.3s; }
    .stButton>button:hover { box-shadow: 0 0 20px #00FF9D; }
</style>
""", unsafe_allow_html=True)

# --- PDF ENGINE (Separate Files) ---
def create_pdf(text, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 14)
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(5)
    pdf.set_font("Times", size=11)
    clean_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    pdf.multi_cell(0, 7, clean_text)
    return pdf.output()

st.markdown("<div class='main-header'>NEURAL ARCHITECT V13: DUAL-INPUT ELITE</div>", unsafe_allow_html=True)

# --- SIDEBAR: PROTOCOLS ---
with st.sidebar:
    st.markdown("### 🔐 ACCESS CONTROL")
    api_key = st.text_input("GROQ API KEY:", type="password")
    st.write("---")
    st.markdown("### 🌍 MARKET PROTOCOL")
    style_choice = st.radio("Apply Standards for:", ["CANADA (Strict ATS)", "USA (Metric Focus)", "EUROPE (Standard)"])
    st.info(f"Target: {style_choice}")

# --- MAIN INTERFACE: DUAL INPUT ---
col_text, col_img = st.columns(2)

with col_text:
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown("#### ⌨️ TEXTUAL DATA / UPDATES")
    st.caption("Paste new experience or additional info here.")
    user_text = st.text_area("Experience / Skills / Job Offer:", height=300, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

with col_img:
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown("#### 🖼️ OLD CV IMAGE / SCAN")
    st.caption("Upload your previous CV image (JPG/PNG/PDF).")
    uploaded_file = st.file_uploader("Drop image here:", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' attached successfully.")
        # Note: In a real OCR setup, we'd extract text here. For now, the Agent is notified.
    st.markdown("</div>", unsafe_allow_html=True)

# --- EXECUTION ---
if st.button("ARCHITECT PRO PACKAGE ⚡", use_container_width=True):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    elif not user_text and not uploaded_file:
        st.warning("Please provide either text info or an old CV file.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.status(f"🧠 Processing {style_choice} Protocol...", expanded=True):
                
                # Full Auto Intelligence with Protocol Guidance
                prompt = f"""
                You are a Professional Career Architect for the {style_choice} market.
                INPUT: {user_text} (Also note: a file named {uploaded_file.name if uploaded_file else 'None'} was uploaded).
                
                STRICT RULES:
                - If CANADA: NO personal sensitive info (age/photo/marital). Focus on STAR achievements.
                - If USA: Metric-heavy (percentages/dollars). Use strong power verbs.
                - If EUROPE: Include skill matrix and language levels.
                
                TASK:
                Generate a Professional CV and a tailored Cover Letter. 
                Use STAR method (Situation, Task, Action, Result) for all points.
                
                OUTPUT FORMAT:
                [CV_START]
                (CV content)
                [CV_END]
                [COVER_START]
                (Cover Letter content)
                [COVER_END]
                """
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                
                content = res.choices[0].message.content
                st.session_state['cv_res'] = content.split("[CV_START]")[1].split("[CV_END]")[0].strip()
                st.session_state['cover_res'] = content.split("[COVER_START]")[1].split("[COVER_END]")[0].strip()
                st.rerun()
        except Exception as e:
            st.error(f"System Error: {e}")

# --- FINAL OUTPUT: SEPARATE VIEWS & DOWNLOADS ---
if 'cv_res' in st.session_state:
    st.write("---")
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.markdown(f"### 📄 {style_choice} CV")
        st.markdown(f"<div class='paper'>{st.session_state['cv_res']}</div>", unsafe_allow_html=True)
        cv_pdf = create_pdf(st.session_state['cv_res'], f"CV - {style_choice} Standard")
        st.download_button("📥 DOWNLOAD CV (PDF)", data=cv_pdf, file_name="My_Professional_CV.pdf", mime="application/pdf", use_container_width=True)

    with res_col2:
        st.markdown(f"### ✉️ {style_choice} COVER LETTER")
        st.markdown(f"<div class='paper'>{st.session_state['cover_res']}</div>", unsafe_allow_html=True)
        cover_pdf = create_pdf(st.session_state['cover_res'], f"Cover Letter - {style_choice}")
        st.download_button("📥 DOWNLOAD COVER LETTER (PDF)", data=cover_pdf, file_name="My_Cover_Letter.pdf", mime="application/pdf", use_container_width=True)
