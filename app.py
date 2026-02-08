import streamlit as st
from groq import Groq
from fpdf import FPDF
import re

# --- UI PRO DESIGN (Mauve & Pro White) ---
st.set_page_config(page_title="CV BOOSTER ELITE V19", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #fcfaff; }
    .main-header { color: #6d28d9; text-align: center; font-weight: 800; font-size: 32px; padding: 15px; border-bottom: 2px solid #e2e8f0; }
    .card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; }
    .preview-paper { background: white; padding: 35px; border-radius: 4px; border: 1px solid #ccc; font-family: 'Helvetica', sans-serif; min-height: 600px; line-height: 1.6; color: #1a1a1a; }
    .stButton>button { background: #7c3aed; color: white; border-radius: 10px; font-weight: bold; height: 55px; width: 100%; border: none; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

# --- ROBUST PDF ENGINE (Fixing Screenshot_288 Error) ---
def create_pdf(text, title):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(109, 40, 217) # Mauve Elite
        pdf.cell(0, 15, title.upper(), ln=True, align='C')
        pdf.set_draw_color(109, 40, 217)
        pdf.line(10, 25, 200, 25) # Horizontal line for pro look
        pdf.ln(10)
        
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(0, 0, 0)
        # Clean text from special characters to prevent encoding errors
        clean_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        pdf.multi_cell(0, 8, clean_text)
        
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        st.error(f"PDF Engine Error: {e}")
        return None

st.markdown("<div class='main-header'>CV BOOSTER AI: PLATINUM ARCHITECT</div>", unsafe_allow_html=True)

# --- SIDEBAR: MANUAL CONFIG ---
with st.sidebar:
    st.markdown("### 🔑 ACCESS")
    api_key_input = st.text_input("Ingresa tu Groq API Key:", type="password")
    st.write("---")
    market = st.radio("Standard Protocol:", ["🇨🇦 CANADA (Strict ATS)", "🇪🇺 EUROPE / MAROC (Professional)"])
    st.info("Logic: STAR Method + Impact-First Verbs")

# --- DUAL TABS (As per your Screenshot_230) ---
tab_file, tab_text = st.tabs(["📤 Subir Archivo (Old CV)", "✍️ Pegar Texto (Job/Info)"])

with tab_file:
    uploaded_file = st.file_uploader("Arrastra tu CV antiguo (PDF/JPG)", type=['pdf', 'jpg', 'png', 'jpeg'], label_visibility="collapsed")

with tab_text:
    user_input = st.text_area("Pega tu información profesional aquí:", height=250, placeholder="Dkhel hna l-khidma dyalk o l-m3loumat...")

# --- PERFORMANCE LOGIC ---
if st.button("GENERAR CV ELITE →", use_container_width=True):
    if not api_key_input:
        st.error("❌ Darouri t-dkhel l-API Key!")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ Lo7 chi m3loumat bach n-khdem.")
    else:
        try:
            client = Groq(api_key=api_key_input)
            with st.status("🚀 Engineering Professional Profile...", expanded=True):
                
                # High-Performance Prompting
                prompt = f"""
                Act as an Elite Career Architect for {market}. 
                The user provided: {user_input if user_input else 'Data from attached file'}.
                
                YOUR MISSION:
                1. CV: Create a high-performance CV. Every bullet point MUST follow the STAR method (Situation, Task, Action, Result). 
                2. Impact: Use Power Verbs (Orchestrated, Spearheaded, Optimized). Focus on MONEY saved or TIME gained.
                3. Structure: 
                   - Professional Summary (High-impact)
                   - Core Competencies (Expertise Grid)
                   - Professional Experience (Action-Result Bullets)
                   - Education & Technical Stack
                4. Cover Letter: A persuasive, emotional, and professional letter tailored to the background.
                
                Format Output:
                [CV_START]
                (Professional CV content)
                [CV_END]
                [COVER_START]
                (Professional Cover Letter content)
                [COVER_END]
                """
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                
                full_resp = res.choices[0].message.content
                st.session_state['cv_p'] = full_resp.split("[CV_START]")[1].split("[CV_END]")[0].strip()
                st.session_state['cover_p'] = full_resp.split("[COVER_START]")[1].split("[COVER_END]")[0].strip()
                st.rerun()
        except Exception as e:
            st.error(f"Engine Failure: {e}")

# --- OUTPUT DISPLAY & DOWNLOADS ---
if 'cv_p' in st.session_state:
    st.write("---")
    col_cv, col_cover = st.columns(2)
    
    with col_cv:
        st.markdown("### 📄 CV OPTIMIZADO (Elite)")
        st.markdown(f"<div class='preview-paper'>{st.session_state['cv_p']}</div>", unsafe_allow_html=True)
        cv_bytes = create_pdf(st.session_state['cv_p'], "Curriculum Vitae")
        if cv_bytes:
            st.download_button("📥 DOWNLOAD CV (PDF)", data=cv_bytes, file_name="Elite_CV.pdf", mime="application/pdf")

    with col_cover:
        st.markdown("### ✉️ CARTA DE PRESENTACIÓN")
        st.markdown(f"<div class='preview-paper'>{st.session_state['cover_p']}</div>", unsafe_allow_html=True)
        cover_bytes = create_pdf(st.session_state['cover_p'], "Cover Letter")
        if cover_bytes:
            st.download_button("📥 DOWNLOAD COVER (PDF)", data=cover_bytes, file_name="Elite_CoverLetter.pdf", mime="application/pdf")
