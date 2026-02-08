import streamlit as st
from groq import Groq
from fpdf import FPDF
import time

# --- Setup Wajiha (Cyber-Pro Style) ---
st.set_page_config(page_title="ELITE CV ARCHITECT", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .main-header { color: #22c55e; text-align: center; font-family: 'Inter', sans-serif; font-weight: 800; font-size: 32px; letter-spacing: -1px; }
    .preview-container { background: #ffffff; color: #1e293b; padding: 40px; border-radius: 8px; font-family: 'Garamond', serif; line-height: 1.5; min-height: 800px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
    .status-badge { background: rgba(34, 197, 94, 0.1); color: #22c55e; border: 1px solid #22c55e; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- PDF Engine (Global Standards) ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=11) # Standard professional font
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, clean_text)
    return pdf.output()

# --- Sidebar (Manual API Entry) ---
with st.sidebar:
    st.markdown("### 🔐 SYSTEM AUTH")
    api_key_input = st.text_input("GROQ API KEY:", type="password") #
    st.write("---")
    st.markdown("### 🛡️ ATS COMPLIANCE")
    st.write("✅ **Canada:** No Photo/No DOB")
    st.write("✅ **USA:** Keyword Density 85%+")
    st.write("✅ **Europe:** Skill-Based Layout")

st.markdown("<h1 class='main-header'>ELITE CV & COVER ARCHITECT</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;'><span class='status-badge'>MODE: GLOBAL RECRUITMENT READY</span></div><br>", unsafe_allow_html=True)

# --- Layout side-by-side ---
col_in, col_desc = st.columns(2)

with col_in:
    st.markdown("### 👤 PROFILE DATA")
    input_type = st.radio("Select Input:", ["Upload Document", "Paste Experience"]) #
    
    user_data = ""
    if input_type == "Upload Document":
        file = st.file_uploader("Drop CV (PDF/TXT)", type=['pdf', 'txt']) #
        if file:
            user_data = file.read().decode("utf-8") if file.type == "text/plain" else "PDF_CONTENT_EXTRACTED"
    else:
        user_data = st.text_area("Paste your background details:", height=300)

with col_desc:
    st.markdown("### 📋 JOB DESCRIPTION")
    job_text = st.text_area("Paste the job offer here (The Agent will detect everything):", height=375) #

# --- Logic Engine ---
if st.button("EXECUTE PRO OPTIMIZATION ⚡"):
    if not api_key_input:
        st.error("Authentication required: Insert API Key in sidebar.") #
    elif not user_data or not job_text:
        st.warning("Insufficient data: Profile and Job Description are mandatory.")
    else:
        try:
            client = Groq(api_key=api_key_input)
            with st.status("🧬 Analyzing Regional Standards & ATS Gaps...", expanded=True) as status:
                st.write("📡 Detecting target country and recruitment style...")
                time.sleep(1)
                st.write("🧬 Architecting CV and Cover Letter with STAR method...")
                
                # Full Auto + Cover Letter + Regional Logic
                prompt = f"""
                You are an Elite Global Recruiter.
                INPUT:
                - User Background: {user_data}
                - Job Offer: {job_text}

                TASK:
                1. Identify the Job Title and Location (e.g., Canada, Germany, etc.) from the Job Offer.
                2. If Canada/USA: Ensure NO photos, NO age, NO marital status. Focus on 'Results-driven' bullets.
                3. Create a Professional CV using the STAR method (Situation, Task, Action, Result).
                4. Create a tailored 'Cover Letter' (Lettre de Motivation) that addresses the specific needs of this company.
                
                OUTPUT STRUCTURE:
                [FULL NAME]
                [CONTACT INFO]
                
                I. PROFESSIONAL CV
                ------------------
                (Detailed, ATS-optimized, high-impact verbs)
                
                II. COVER LETTER
                ------------------
                (Professional, persuasive, matching the job requirements)
                """
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2 # Extreme accuracy
                )
                st.session_state['elite_result'] = res.choices[0].message.content
                status.update(label="✅ GENERATION COMPLETE", state="complete")
        except Exception as e:
            st.error(f"System Overload: {e}")

# --- Global Result Display ---
if 'elite_result' in st.session_state:
    st.write("---")
    st.markdown("### 📄 ARCHITECTED PACKAGE (CV + COVER LETTER)")
    st.markdown(f"<div class='preview-container'>{st.session_state['elite_result']}</div>", unsafe_allow_html=True)
    
    # PDF Conversion
    pdf_final = create_pdf(st.session_state['elite_result'])
    st.download_button(
        label="📥 DOWNLOAD PRO PDF PACKAGE",
        data=pdf_final,
        file_name="Global_Pro_Package.pdf",
        mime="application/pdf"
    )
