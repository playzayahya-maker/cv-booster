import streamlit as st
from groq import Groq
from fpdf import FPDF
import re

# --- UI Setup (Elite Pro) ---
st.set_page_config(page_title="ATS ELITE ARCHITECT", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #010409; color: #e6edf3; }
    .main-header { color: #238636; text-align: center; font-size: 35px; font-weight: 800; padding: 20px; }
    .paper { background: white; color: #1a1a1a; padding: 35px; border-radius: 4px; font-family: 'Times New Roman', serif; min-height: 700px; box-shadow: 0 10px 40px rgba(0,0,0,0.6); line-height: 1.5; }
    .section-header { color: #238636; font-size: 22px; font-weight: bold; margin-bottom: 15px; border-bottom: 2px solid #238636; }
    .stButton>button { background: #238636; color: white; border-radius: 8px; font-weight: bold; height: 50px; border: none; }
    .style-box { background: #0d1117; padding: 20px; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- PDF Engine (Stable) ---
def generate_ats_package(cv_text, cover_text):
    pdf = FPDF()
    # Page 1: CV
    pdf.add_page()
    pdf.set_font("Times", 'B', 16)
    pdf.cell(0, 10, "CURRICULUM VITAE", ln=True, align='C')
    pdf.set_font("Times", size=11)
    pdf.multi_cell(0, 8, re.sub(r'[^\x00-\x7F]+', ' ', cv_text))
    # Page 2: Cover Letter
    pdf.add_page()
    pdf.set_font("Times", 'B', 16)
    pdf.cell(0, 10, "COVER LETTER", ln=True, align='C')
    pdf.set_font("Times", size=11)
    pdf.multi_cell(0, 8, re.sub(r'[^\x00-\x7F]+', ' ', cover_text))
    return pdf.output()

st.markdown("<div class='main-header'>ATS NEURAL ARCHITECT V10</div>", unsafe_allow_html=True)

# --- Selection & Input ---
with st.sidebar:
    st.markdown("### 🔐 SYSTEM KEY")
    api_key = st.text_input("GROQ API KEY:", type="password")
    st.write("---")
    st.markdown("### 🌍 SELECT TARGET STYLE")
    # Had l-boutonat darouriyin bach l-Agent i-3ref chnu i-dir
    target_style = st.radio("Style Protocol:", ["CANADA", "USA", "EUROPE"])
    st.info(f"Protocol {target_style} is now ACTIVE.")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### 📥 SOURCE DATA (CV + JOB)")
    mega_input = st.text_area("Paste your background and the job description here:", height=400, placeholder="The Agent will auto-detect which is which...")

with col2:
    st.markdown("#### 🛡️ STYLE RULES")
    if target_style == "CANADA":
        st.write("❌ No Photo / No Age / No Personal Bio")
        st.write("✅ Reverse Chronological Only")
        st.write("✅ STAR Method Focused")
        
    elif target_style == "USA":
        st.write("✅ Metric-Heavy (Numbers & %)")
        st.write("✅ Professional Summary (Max 3 lines)")
        st.write("✅ Keywords Matching 95%+")
        
    else:
        st.write("✅ Europass/Modern Skills Layout")
        st.write("✅ Personal Statement Included")
        st.write("✅ Soft & Hard Skills Balanced")
        

# --- Neural Logic ---
if st.button("START ELITE OPTIMIZATION ⚡", use_container_width=True):
    if not api_key:
        st.error("Please enter the API Key in Sidebar.")
    elif not mega_input:
        st.warning("Input is empty.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.status(f"🧬 Applying {target_style} Standards...", expanded=True):
                
                # Dynamic Prompt based on selection
                prompt = f"""
                You are a Senior Recruiter expert in {target_style} market standards.
                INPUT: {mega_input}
                
                STRICT PROTOCOL FOR {target_style}:
                - If CANADA: Strictly NO photos, NO marital status, NO birthdate. Use Reverse Chronological. Focus on STAR achievements.
                - If USA: Focus on quantifiable results ($ and %). Short professional summary. High keyword density.
                - If EUROPE: Use modern Europass structure. Include a personal statement and clear skill sections.
                
                OUTPUT STRUCTURE (Must follow this exactly):
                [CV_START]
                (Professional CV content here)
                [CV_END]
                [COVER_START]
                (Tailored Cover Letter here)
                [COVER_END]
                """
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                
                out = res.choices[0].message.content
                st.session_state['cv'] = out.split("[CV_START]")[1].split("[CV_END]")[0].strip()
                st.session_state['cover'] = out.split("[COVER_START]")[1].split("[COVER_END]")[0].strip()
                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# --- Results ---
if 'cv' in st.session_state:
    st.write("---")
    res_cv, res_cover = st.columns(2)
    
    with res_cv:
        st.markdown(f"<div class='section-header'>📄 {target_style} CV</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='paper'>{st.session_state['cv']}</div>", unsafe_allow_html=True)
        
    with res_cover:
        st.markdown(f"<div class='section-header'>✉️ {target_style} COVER LETTER</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='paper'>{st.session_state['cover']}</div>", unsafe_allow_html=True)
    
    # PDF Package
    pdf_final = generate_ats_package(st.session_state['cv'], st.session_state['cover'])
    st.download_button(
        label="📥 DOWNLOAD ATS PDF PACKAGE",
        data=pdf_final,
        file_name=f"Elite_{target_style}_Package.pdf",
        mime="application/pdf",
        use_container_width=True
    )
