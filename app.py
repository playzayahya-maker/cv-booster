import streamlit as st
from groq import Groq
from fpdf import FPDF
import time
import re

# --- UI CONFIG ---
st.set_page_config(page_title="ATS ARCHITECT ELITE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #020617; color: #f1f5f9; }
    .main-header { color: #10b981; text-align: center; font-size: 38px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Neon Selection Bar */
    .stSelectbox, .stRadio { background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; }
    
    /* Paper Design for CV & Cover Letter */
    .paper { background: white; color: #1e293b; padding: 40px; border-radius: 4px; font-family: 'Times', serif; box-shadow: 0 10px 40px rgba(0,0,0,0.5); margin-bottom: 20px; }
    .paper-title { color: #10b981; font-weight: bold; margin-bottom: 15px; border-bottom: 2px solid #10b981; padding-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# --- PDF ENGINE (ULTRA STABLE) ---
def generate_ats_pdf(cv_text, cover_text):
    pdf = FPDF()
    # Page 1: CV
    pdf.add_page()
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 10, "CURRICULUM VITAE (ATS OPTIMIZED)", ln=True, align='C')
    pdf.set_font("Times", size=11)
    # Clean emojis & non-latin
    clean_cv = re.sub(r'[^\x00-\x7F]+', ' ', cv_text)
    pdf.multi_cell(0, 8, clean_cv)
    
    # Page 2: Cover Letter
    pdf.add_page()
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 10, "PROFESSIONAL COVER LETTER", ln=True, align='C')
    pdf.set_font("Times", size=11)
    clean_cover = re.sub(r'[^\x00-\x7F]+', ' ', cover_text)
    pdf.multi_cell(0, 8, clean_cover)
    
    return pdf.output()

# --- SIDEBAR & API ---
with st.sidebar:
    st.markdown("### 🔐 AUTHENTICATION")
    api_key = st.text_input("ENTER GROQ KEY:", type="password")
    st.write("---")
    st.markdown("### 🛡️ ATS COMPLIANCE")
    st.caption("Active Mode: Anti-Rejection")

st.markdown("<div class='main-header'>ATS ARCHITECT ELITE V8</div>", unsafe_allow_html=True)

# --- STYLE & INPUT SELECTION ---
col_s, col_m = st.columns([1, 2])
with col_s:
    st.markdown("#### 🌍 TARGET MARKET")
    style_choice = st.radio("Apply Strict Rules for:", ["CANADA (No Photo, Reverse Chrono)", "USA (Metric-Heavy)", "EUROPE (Modern Professional)"])

with col_m:
    st.markdown("#### 📥 DATA SOURCE")
    input_choice = st.radio("Input Type:", ["Smart Box (Paste All)", "Upload Document"], horizontal=True)

st.markdown("---")

user_raw_data = ""
if input_choice == "Smart Box (Paste All)":
    user_raw_data = st.text_area("Paste your CV Content AND the Job Description here:", height=300)
else:
    f = st.file_uploader("Upload CV (PDF/TXT):", type=['pdf', 'txt'])
    jd = st.text_area("Paste Job Offer Details:", height=150)
    if f and jd:
        user_raw_data = f"CV CONTENT: {f.name} \n\n TARGET JOB OFFER: {jd}"

# --- EXECUTION ---
if st.button("EXECUTE NEURAL ARCHITECT ⚡", use_container_width=True):
    if not api_key:
        st.error("Missing API Key.")
    elif len(user_raw_data) < 50:
        st.warning("Insufficient data. Please paste both your background and the job offer.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.status("🧠 Processing...", expanded=True):
                # Prompt m-qadd dial s-se7
                prompt = f"""
                Act as a Senior Executive Career Architect. 
                Target Market Style: {style_choice}
                
                Input: {user_raw_data}
                
                MISSION:
                1. Split input into CV and Job Description.
                2. Re-write the CV following STRICT {style_choice} standards. 
                   - Use STAR method for achievements.
                   - Ensure 90%+ keyword matching.
                   - NO personal info like age/photo if Canada/USA.
                3. Write a high-conversion Cover Letter tailored to the specific job and company.
                
                Format your response EXACTLY like this:
                ---CV_START---
                [CV content here]
                ---CV_END---
                ---COVER_START---
                [Cover Letter content here]
                ---COVER_END---
                """
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1 # Precision mode
                )
                
                full_res = res.choices[0].message.content
                # Parse CV and Cover
                st.session_state['cv_part'] = full_res.split("---CV_START---")[1].split("---CV_END---")[0].strip()
                st.session_state['cover_part'] = full_res.split("---COVER_START---")[1].split("---COVER_END---")[0].strip()
                st.rerun()

        except Exception as e:
            st.error(f"Engine Error: {e}")

# --- RESULTS DISPLAY ---
if 'cv_part' in st.session_state:
    col_cv, col_cover = st.columns(2)
    
    with col_cv:
        st.markdown("<div class='paper-title'>📄 ATS CV (CANADA/GLOBAL STYLE)</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='paper'>{st.session_state['cv_part']}</div>", unsafe_allow_html=True)
        
    with col_cover:
        st.markdown("<div class='paper-title'>✉️ TAILORED COVER LETTER</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='paper'>{st.session_state['cover_part']}</div>", unsafe_allow_html=True)
    
    # PDF EXPORT
    try:
        pdf_bytes = generate_ats_pdf(st.session_state['cv_part'], st.session_state['cover_part'])
        st.download_button(
            label="📥 DOWNLOAD FULL PACKAGE (PDF)",
            data=pdf_bytes,
            file_name=f"Elite_Career_Package_{style_choice.split()[0]}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"PDF Generator Error: {e}")
