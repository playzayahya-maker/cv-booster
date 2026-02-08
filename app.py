import streamlit as st
from groq import Groq
from fpdf import FPDF
import re

# --- CONFIG & DESIGN (Colors: Mauve, White, Indigo) ---
st.set_page_config(page_title="CV BOOSTER PRO", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #fcfaff; color: #334155; }
    .main-header { color: #6d28d9; text-align: center; font-weight: 800; font-size: 32px; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #ffffff; border-radius: 10px; padding: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab"] { font-weight: 600; color: #6b7280; }
    .stTabs [aria-selected="true"] { color: #6d28d9 !important; border-bottom-color: #6d28d9 !important; }
    .preview-paper { background: white; padding: 40px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05); color: #1e293b; font-family: 'Times', serif; }
    .stButton>button { background: #7c3aed; color: white; border-radius: 10px; font-weight: bold; border: none; height: 55px; font-size: 18px; }
    .stButton>button:hover { background: #6d28d9; box-shadow: 0 0 15px rgba(124, 58, 237, 0.4); }
</style>
""", unsafe_allow_html=True)

# --- PDF GENERATOR (Dual Engine) ---
def create_pdf(text, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 16)
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", size=11)
    clean_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    pdf.multi_cell(0, 8, clean_text)
    return pdf.output(dest='S').encode('latin-1')

st.markdown("<div class='main-header'>CV BOOSTER: SMART OPTIMIZER</div>", unsafe_allow_html=True)

# --- SIDEBAR: API KEY MANUAL & STYLE ---
with st.sidebar:
    st.markdown("### 🔑 CONFIGURATION")
    # API Key Manual Input
    api_key_input = st.text_input("Ingresa tu Groq API Key:", type="password", help="Dkhel l-Key dyalk hna bach t-khdem l-IA")
    
    st.write("---")
    st.markdown("### 🌍 SELECCIONAR MERCADO")
    market = st.radio("Destino:", ["🇨🇦 CANADA (Strict ATS)", "🇪🇺 EUROPE (Standard)"])
    
    st.write("---")
    st.caption("Protocolo activo: STAR Achievement & Anti-Bias Filtering")

# --- MAIN INPUT TABS (The design you circled) ---
# Separated into 'Subir Archivo' and 'Pegar Texto'
tab1, tab2 = st.tabs(["📤 Subir Archivo", "✍️ Pegar Texto"])

with tab1:
    st.markdown("#### Arrastra tu CV antiguo aquí")
    uploaded_file = st.file_uploader("Soportado: PDF, JPG, PNG", type=['pdf', 'jpg', 'png', 'jpeg'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"Archivo '{uploaded_file.name}' cargado con éxito.")

with tab2:
    st.markdown("#### Pega el contenido o la descripción del trabajo")
    user_input = st.text_area("Contenido del CV o Job Description:", height=250, placeholder="Escribe o pega aquí...", label_visibility="collapsed")

# --- PROCESS BUTTON ---
if st.button("GENERAR CV OPTIMIZADO →", use_container_width=True):
    if not api_key_input:
        st.error("❌ Error: Darouri t-dkhel l-API Key f l-sidebar bach n-bdaw.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ Warning: Lo7 chi info f l-tabs sghiba.")
    else:
        try:
            client = Groq(api_key=api_key_input)
            with st.status(f"🧠 Optimizando para {market}...", expanded=True):
                
                prompt = f"""
                You are a career consultant for {market}. 
                Data: {user_input if user_input else 'Data extracted from file'}
                
                Strict Rules:
                - If CANADA: Format as seen in professional Canadian resumes (No photo, Reverse Chronological, STAR method bullets). 
                - If EUROPE: Focus on Core Competencies grid, Skills Matrix, and Languages. 
                - Both: Write a professional Cover Letter.
                
                Format Output as:
                [CV_START]
                (CV Content)
                [CV_END]
                [COVER_START]
                (Cover Letter Content)
                [COVER_END]
                """
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                
                full_resp = res.choices[0].message.content
                st.session_state['cv_final'] = full_resp.split("[CV_START]")[1].split("[CV_END]")[0].strip()
                st.session_state['cover_final'] = full_resp.split("[COVER_START]")[1].split("[COVER_END]")[0].strip()
                st.rerun()
        except Exception as e:
            st.error(f"Engine Error: {e}")

# --- RESULTS & SEPARATE DOWNLOADS ---
if 'cv_final' in st.session_state:
    st.write("---")
    col_cv, col_cover = st.columns(2)
    
    with col_cv:
        st.markdown("### 📄 CV OPTIMIZADO")
        st.markdown(f"<div class='preview-paper'>{st.session_state['cv_final']}</div>", unsafe_allow_html=True)
        cv_pdf = create_pdf(st.session_state['cv_final'], "CURRICULUM VITAE")
        st.download_button("📥 Download CV (PDF)", data=cv_pdf, file_name="CV_Optimized.pdf", mime="application/pdf", use_container_width=True)

    with col_cover:
        st.markdown("### ✉️ CARTA DE PRESENTACIÓN")
        st.markdown(f"<div class='preview-paper'>{st.session_state['cover_final']}</div>", unsafe_allow_html=True)
        cover_pdf = create_pdf(st.session_state['cover_final'], "COVER LETTER")
        st.download_button("📥 Download Cover Letter (PDF)", data=cover_pdf, file_name="Cover_Letter.pdf", mime="application/pdf", use_container_width=True)
