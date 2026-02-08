import streamlit as st
from groq import Groq
from fpdf import FPDF
import pdfplumber
import re

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="CV BOOSTER ELITE V25", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #fcfaff; }
    .main-header { color: #6d28d9; text-align: left; font-weight: 800; font-size: 30px; padding: 15px; border-bottom: 2px solid #e2e8f0; }
    .preview-paper { background: white; padding: 35px; border-radius: 4px; border: 1px solid #ddd; font-family: 'Helvetica', sans-serif; min-height: 500px; color: #1a1a1a; line-height: 1.5; }
    .stButton>button { background: #7c3aed; color: white; border-radius: 10px; font-weight: bold; height: 55px; width: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 2. ROBUST PDF ENGINE (UTF-8 + No Crash) ---
class PDF(FPDF):
    def header(self):
        pass # Custom header if needed

def generate_pdf_file(text, title, market):
    pdf = FPDF()
    pdf.add_page()
    # Header Style
    pdf.set_font("Helvetica", 'B', 16)
    pdf.set_text_color(109, 40, 217) # Mauve
    align = 'L' if market == "CANADA" else 'C'
    pdf.cell(0, 10, title.upper(), ln=True, align=align)
    pdf.line(10, 22, 200, 22)
    pdf.ln(10)
    # Content Style
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(0, 0, 0)
    # FPDF2 handles UTF-8 automatically
    pdf.multi_cell(0, 7, text)
    return pdf.output()

# --- 3. EXTRACTION ENGINE ---
def extract_pdf_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

st.markdown("<div class='main-header'>🚀 CV BOOSTER <span style='color:#94a3b8; font-size:14px;'>FINAL V25</span></div>", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔑 ACCESS & SETTINGS")
    api_key = st.text_input("Groq API Key:", type="password")
    market = st.selectbox("Target Country:", ["Canada", "Germany", "France", "Spain", "Italy", "UK"])
    st.write("---")
    st.info("Logic: STAR Method + No Skill Levels + UTF-8 Safe.")

# --- 5. INPUT TABS (As per Screenshot_230) ---
tab_file, tab_text = st.tabs(["📤 Subir Archivo", "✍️ Pegar Texto"])
final_input_text = ""

with tab_file:
    up_file = st.file_uploader("Upload PDF CV", type=['pdf'], label_visibility="collapsed")
    if up_file:
        final_input_text = extract_pdf_text(up_file)
        st.success("PDF Content Extracted.")

with tab_text:
    user_text = st.text_area("Experience/Skills:", height=250, placeholder="Paste details here...", label_visibility="collapsed")
    if user_text:
        final_input_text += "\n" + user_text

# --- 6. PERFORMANCE EXECUTION ---
if st.button("ARCHITECT CV & COVER LETTER →", use_container_width=True):
    if not api_key:
        st.error("API Key is missing!")
    elif not final_input_text:
        st.warning("Please provide CV data.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.status(f"🧠 Optimizing for {market}..."):
                
                system_prompt = f"""
                You are a Senior Career Architect in {market}.
                RULES:
                1. Include Phone (+212) and Location (Casablanca, Morocco).
                2. Skills: Simple list (SQL, Power BI, ETL). NO levels like 'Advanced'.
                3. Experience: Use STAR method (Action + Task + Result).
                4. Languages: If Europe, use CEFR (A1-C1). If Canada, focus on 'Mots-clés'.
                5. Output: Strictly separate CV and Cover inside tags.
                """
                
                user_msg = f"Data: {final_input_text}. Return strictly in: [CV_START]...[CV_END] and [COVER_START]...[COVER_END]"
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
                    temperature=0.1
                )
                
                raw = res.choices[0].message.content
                if "[CV_START]" in raw and "[COVER_START]" in raw:
                    st.session_state['cv_res'] = raw.split("[CV_START]")[1].split("[CV_END]")[0].strip()
                    st.session_state['cover_res'] = raw.split("[COVER_START]")[1].split("[COVER_END]")[0].strip()
                else:
                    st.error("Format Error. Please try again.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- 7. SEPARATE DISPLAYS & DOWNLOADS (Fixing Screenshot_288) ---
if 'cv_res' in st.session_state:
    st.write("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### 📄 CV OPTIMIZADO ({market})")
        st.markdown(f"<div class='preview-paper'>{st.session_state['cv_res']}</div>", unsafe_allow_html=True)
        # Fix: Generate PDF bytes directly in the download button logic
        cv_pdf = generate_pdf_file(st.session_state['cv_res'], "Curriculum Vitae", market.upper())
        st.download_button("📥 DOWNLOAD CV (PDF)", data=cv_pdf, file_name=f"CV_{market}.pdf", mime="application/pdf")

    with col2:
        st.markdown("#### ✉️ CARTA DE PRESENTACIÓN")
        st.markdown(f"<div class='preview-paper'>{st.session_state['cover_res']}</div>", unsafe_allow_html=True)
        cover_pdf = generate_pdf_file(st.session_state['cover_res'], "Cover Letter", market.upper())
        st.download_button("📥 DOWNLOAD COVER (PDF)", data=cover_pdf, file_name=f"Cover_{market}.pdf", mime="application/pdf")
