import streamlit as st
from groq import Groq
import pdfplumber
from fpdf import FPDF
import io

# --- 1. CONFIGURATION B7AL L-PHOTO ---
st.set_page_config(page_title="CV Booster Pro", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f4f7fe; }
    .main-header { color: #4f46e5; font-weight: 800; font-size: 28px; margin-bottom: 20px; }
    /* Style dial s-sora */
    .preview-card { background: white; padding: 30px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); font-family: 'Helvetica'; color: #1e293b; }
    .stButton>button { background: #4f46e5; color: white; border-radius: 8px; font-weight: bold; height: 50px; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 2. FIXED PDF ENGINE (No more StreamlitAPIException) ---
def generate_safe_pdf(text, title, market):
    pdf = FPDF()
    pdf.add_page()
    # Header Style b7al Screenshot 233
    pdf.set_font("Helvetica", 'B', 16)
    pdf.set_text_color(79, 70, 229) 
    pdf.cell(0, 10, title.upper(), ln=True, align='L' if market == "Canada" else 'C')
    pdf.line(10, 22, 200, 22)
    pdf.ln(10)
    
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(30, 41, 59)
    # Fix dial encoding bach may-crachich
    safe_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    
    # OUTPUT AS BYTES (Fix dial Screenshot 291)
    return bytes(pdf.output())

# --- 3. UI LAYOUT B7AL SCREENSHOT 230 ---
st.markdown("<div class='main-header'>📑 CV Booster Pro</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Groq API Key:", type="password")
    market = st.selectbox("Target Market:", ["Canada", "France", "Germany", "UK", "Spain"])
    st.write("---")
    st.info("Protocol: ATS-Friendly + STAR Achievements.")

# Tabs b7al s-tsora
tab_upload, tab_paste = st.tabs(["📤 Subir Archivo", "✍️ Pegar Texto"])
input_text = ""

with tab_upload:
    up_file = st.file_uploader("Upload CV (PDF)", type=['pdf'], label_visibility="collapsed")
    if up_file:
        with pdfplumber.open(up_file) as pdf:
            input_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

with tab_paste:
    paste_text = st.text_area("Pega el contenido de tu CV aquí:", height=250, label_visibility="collapsed")
    if paste_text:
        input_text = paste_text

# --- 4. GENERATION LOGIC ---
if st.button("GENERAR CV Y COVER LETTER OPTIMIZADO →"):
    if not api_key or not input_text:
        st.error("Please provide API Key and Data.")
    else:
        try:
            client = Groq(api_key=api_key)
            # Prompt m-fignoli bach i-3ti CV o Cover Letter m-separeryn
            system_msg = f"Expert Recruiter for {market}. Create a Professional CV and a tailored Cover Letter. Use [CV_DOC] and [LETTER_DOC] as separators."
            
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"{system_msg}\n\nData: {input_text}"}],
                temperature=0.2
            )
            raw_res = res.choices[0].message.content
            
            # Parsing
            st.session_state.cv_final = raw_res.split("[CV_DOC]")[1].split("[LETTER_DOC]")[0].strip()
            st.session_state.letter_final = raw_res.split("[LETTER_DOC]")[1].strip()
        except Exception as e:
            st.error(f"AI Error: {e}")

# --- 5. RESULTS DISPLAY (Separation Mode) ---
if 'cv_final' in st.session_state:
    st.divider()
    col_cv, col_letter = st.columns(2)
    
    with col_cv:
        st.subheader("📄 Curriculum Vitae")
        st.markdown(f"<div class='preview-card'>{st.session_state.cv_final}</div>", unsafe_allow_html=True)
        cv_pdf = generate_safe_pdf(st.session_state.cv_final, "Curriculum Vitae", market)
        st.download_button("📥 Download CV", data=cv_pdf, file_name=f"CV_{market}.pdf", mime="application/pdf")

    with col_letter:
        # L-jiha d l-cover li kant khassa
        st.subheader("✉️ Carta de Presentación")
        st.markdown(f"<div class='preview-card'>{st.session_state.letter_final}</div>", unsafe_allow_html=True)
        letter_pdf = generate_safe_pdf(st.session_state.letter_final, "Cover Letter", market)
        st.download_button("📥 Download Letter", data=letter_pdf, file_name=f"Cover_{market}.pdf", mime="application/pdf")
