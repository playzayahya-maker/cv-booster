import streamlit as st
from groq import Groq
from fpdf import FPDF
import pdfplumber
import re

# --- UI DESIGN (Mauve & White Style) ---
st.set_page_config(page_title="CV BOOSTER ELITE V23", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #fcfaff; color: #1e293b; }
    .main-header { color: #6d28d9; text-align: left; font-weight: 800; font-size: 30px; padding: 15px; border-bottom: 2px solid #e2e8f0; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: white; border-radius: 10px; padding: 10px 20px; border: 1px solid #e2e8f0; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #7c3aed !important; color: white !important; }
    .preview-paper { background: white; padding: 40px; border-radius: 4px; border: 1px solid #ddd; box-shadow: 0 4px 12px rgba(0,0,0,0.05); font-family: 'Helvetica', sans-serif; min-height: 600px; color: #1a1a1a; }
    .stButton>button { background: #7c3aed; color: white; border-radius: 10px; font-weight: bold; height: 55px; width: 100%; border: none; font-size: 18px; }
    .stButton>button:hover { background: #6d28d9; box-shadow: 0 0 15px rgba(124, 58, 237, 0.4); }
</style>
""", unsafe_allow_html=True)

# --- PDF ENGINE (UTF-8 & NO-CRASH) ---
def create_pdf(text, title, market_type):
    pdf = FPDF()
    pdf.add_page()
    # Header Styling
    pdf.set_font("Helvetica", 'B', 16)
    pdf.set_text_color(109, 40, 217) # Mauve
    align = 'L' if market_type == "CANADA" else 'C'
    pdf.cell(0, 10, title.upper(), ln=True, align=align)
    pdf.line(10, 25, 200, 25)
    pdf.ln(10)
    # Content Styling
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(0, 0, 0)
    # Safe multi-cell for UTF-8 (fpdf2 handles this)
    pdf.multi_cell(0, 7, text)
    return pdf.output()

# --- EXTRACTION ENGINE (PDF-to-Text) ---
def get_pdf_content(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

st.markdown("<div class='main-header'>🚀 CV BOOSTER <span style='color:#94a3b8; font-size:14px;'>ELITE V23</span></div>", unsafe_allow_html=True)

# --- SIDEBAR CONFIG ---
with st.sidebar:
    st.markdown("### 🔑 ACCESS CONTROL")
    api_key = st.text_input("Groq API Key:", type="password", placeholder="gsk_...")
    st.write("---")
    market = st.radio("Target Protocol:", ["CANADA", "EUROPE"])
    st.write("---")
    st.caption("Standard: Anti-Bias, STAR Method, Performance Metrics")

# --- DUAL TABS INTERFACE ---
tab_file, tab_text = st.tabs(["📤 Subir Archivo", "✍️ Pegar Texto"])
raw_content = ""

with tab_file:
    uploaded_file = st.file_uploader("Upload Old CV (PDF)", type=['pdf'], label_visibility="collapsed")
    if uploaded_file:
        raw_content = get_pdf_content(uploaded_file)
        st.success("PDF Content Extracted Successfully.")

with tab_text:
    user_text = st.text_area("Experience / Skills / Job Info:", height=250, placeholder="Paste data here...", label_visibility="collapsed")
    if user_text:
        raw_content += "\n" + user_text

# --- ENGINE EXECUTION ---
if st.button("ARCHITECT PROFESSIONAL PROFILE →", use_container_width=True):
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not raw_content:
        st.warning("No data found to optimize.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.status(f"🧠 Engineering {market} Standards..."):
                
                # Role-Based Master Prompt
                system_prompt = f"""
                You are a Master Career Consultant for the {market} market. 
                STRICT GUIDELINES:
                - Phone: Always include +212. Location: Casablanca, Morocco.
                - Keywords: Data Cleaning, ETL, Predictive Modeling, Power BI.
                - Skills: List them simply. NO labels like 'Advanced', 'Expert', or 'Level 5'.
                - Bullets: Use the STAR method (Situation, Task, Action, Result) with strong Power Verbs.
                - Hyperlink: Ensure LinkedIn is formatted as a URL.
                
                IF CANADA: Single column ONLY. No personal info (DOB/Photo). Reverse chronological.
                IF EUROPE: Include 'Languages' with CEFR levels (A1-C1). Add a section for 'Hobbies/Interests'.
                """
                
                user_msg = f"Optimize this content: {raw_content}. Provide output strictly within [CV_START][CV_END] and [COVER_START][COVER_END]."

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=0.1
                )
                
                output = res.choices[0].message.content
                
                # Robust Parsing
                if "[CV_START]" in output and "[COVER_START]" in output:
                    st.session_state['final_cv'] = output.split("[CV_START]")[1].split("[CV_END]")[0].strip()
                    st.session_state['final_cover'] = output.split("[COVER_START]")[1].split("[COVER_END]")[0].strip()
                else:
                    st.error("AI Formatting Error. Please try again.")

        except Exception as e:
            st.error(f"Engine Failure: {e}")

# --- DISPLAY & SEPARATE DOWNLOADS ---
if 'final_cv' in st.session_state:
    st.write("---")
    col_cv, col_cover = st.columns(2)
    
    with col_cv:
        st.markdown("#### 📄 OPTIMIZED CV")
        st.markdown(f"<div class='preview-paper'>{st.session_state['final_cv']}</div>", unsafe_allow_html=True)
        cv_bytes = create_pdf(st.session_state['final_cv'], "Curriculum Vitae", market)
        st.download_button("📥 DOWNLOAD CV (PDF)", data=cv_bytes, file_name="Professional_CV.pdf", mime="application/pdf")

    with col_cover:
        st.markdown("#### ✉️ PERSUASIVE COVER LETTER")
        st.markdown(f"<div class='preview-paper'>{st.session_state['final_cover']}</div>", unsafe_allow_html=True)
        cover_bytes = create_pdf(st.session_state['final_cover'], "Cover Letter", market)
        st.download_button("📥 DOWNLOAD COVER (PDF)", data=cover_bytes, file_name="Cover_Letter.pdf", mime="application/pdf")
