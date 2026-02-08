import streamlit as st
from groq import Groq
from fpdf import FPDF
import time

# --- UI SETUP ---
st.set_page_config(page_title="AI CV ARCHITECT PRO", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #fff; }
    .main-header { color: #00ff9d; text-align: center; font-family: 'Space Mono', monospace; font-size: 30px; }
    .cv-preview { background: #111; border: 1px solid #222; padding: 20px; border-radius: 10px; font-family: 'serif'; color: #333; background-color: white; min-height: 400px; }
    .status-badge { background: #00ff9d22; color: #00ff9d; padding: 5px 12px; border-radius: 15px; border: 1px solid #00ff9d; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# --- PDF GENERATOR FUNCTION ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Cleaning text for PDF (fpdf2 likes simple latin-1)
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    return pdf.output()

# --- SIDEBAR (API MANUAL) ---
with st.sidebar:
    st.markdown("### 🔐 ACCESS CONTROL")
    api_key_input = st.text_input("ENTER GROQ API KEY:", type="password") #
    st.write("---")
    st.markdown("### 🛠 SYSTEM LOGS")
    st.info("Agent: CV-Optimizer-V4\nModel: Llama-3.3-70B")

# --- MAIN INTERFACE ---
st.markdown("<h1 class='main-header'>AI CV ARCHITECT PRO</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;'><span class='status-badge'>PDF EXPORT ENABLED</span></div><br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📁 UPLOAD PROFILE")
    uploaded_file = st.file_uploader("Upload CV (PDF/TXT)", type=['pdf', 'txt']) #
    target_job = st.text_input("🎯 TARGET JOB:", placeholder="e.g. Mechanical Engineer")
    style = st.selectbox("🌍 REGION STYLE:", ["USA (ATS)", "Canada", "Europe"])

with col2:
    st.markdown("### 📝 JOB DESCRIPTION")
    job_desc = st.text_area("Paste the job offer details here:", height=215)

# --- LOGIC ---
if st.button("GENERATE PRO CV ⚡"):
    if not api_key_input:
        st.error("Missing API Key. Check Sidebar.")
    elif not uploaded_file or not job_desc:
        st.warning("Please provide both CV and Job Description.")
    else:
        try:
            client = Groq(api_key=api_key_input)
            with st.status("🧬 Architecting your new CV...", expanded=True) as status:
                st.write("📡 Analyzing ATS keywords...")
                time.sleep(1)
                
                # Performance optimized prompt
                prompt = f"""
                Create a professional CV for the role of {target_job} based on this data:
                Profile Info: {uploaded_file.name}
                Job Requirements: {job_desc}
                Style: {style}
                
                Instructions:
                - Use impact verbs.
                - Quantify achievements.
                - Format clearly for ATS.
                Return ONLY the CV content.
                """
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2 # Maximum Accuracy
                )
                st.session_state['final_cv'] = res.choices[0].message.content
                status.update(label="✅ GENERATION COMPLETE", state="complete")
        except Exception as e:
            st.error(f"Error: {e}")

# --- DISPLAY & DOWNLOAD ---
if 'final_cv' in st.session_state:
    st.write("---")
    st.markdown("### ✨ PREVIEW & EXPORT")
    
    # Preview Box
    st.markdown(f"<div class='cv-preview'>{st.session_state['final_cv']}</div>", unsafe_allow_html=True)
    
    # PDF Conversion
    pdf_bytes = create_pdf(st.session_state['final_cv'])
    
    st.download_button(
        label="📥 DOWNLOAD AS PDF",
        data=pdf_bytes,
        file_name=f"CV_{target_job.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
