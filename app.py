import streamlit as st
from groq import Groq
from fpdf import FPDF
import pdfplumber

# --- UI & Layout ---
st.set_page_config(page_title="CV & Cover Letter Pro", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .main-header { color: #6d28d9; font-weight: 800; font-size: 32px; margin-bottom: 20px; }
    .card { background: white; padding: 30px; border-radius: 12px; border: 1px solid #e2e8f0; min-height: 450px; }
    .stButton>button { background: #7c3aed; color: white; border-radius: 8px; font-weight: bold; height: 50px; width: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# --- Function for PDF (UTF-8) ---
def build_pdf(content, title, market):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.set_text_color(109, 40, 217) # Mauve Style
    pdf.cell(0, 10, title.upper(), ln=True, align='L' if market == "Canada" else 'C')
    pdf.line(10, 22, 200, 22)
    pdf.ln(10)
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(0, 7, content)
    return pdf.output()

# --- Extraction Logic ---
def get_pdf_text(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

st.markdown("<div class='main-header'>🚀 Pro Career Suite V27</div>", unsafe_allow_html=True)

# --- Inputs ---
with st.sidebar:
    st.header("⚙️ Settings")
    key = st.text_input("Groq API Key:", type="password")
    dest = st.selectbox("Market:", ["Canada", "Germany", "France", "UK", "Spain", "Italy"])

# UI Tabs for Input
t1, t2 = st.tabs(["📤 Upload PDF CV", "✍️ Paste Content"])
raw_text = ""
with t1:
    f = st.file_uploader("Upload current CV", type=['pdf'], label_visibility="collapsed")
    if f: raw_text = get_pdf_text(f)
with t2:
    txt = st.text_area("Paste experience here...", height=200, label_visibility="collapsed")
    if txt: raw_text += "\n" + txt

# --- AI Logic ---
if st.button("GENERATE CV + COVER LETTER"):
    if not key or not raw_text:
        st.error("Missing Data/Key.")
    else:
        try:
            client = Groq(api_key=key)
            prompt = f"""
            Role: Expert Career Coach in {dest}. 
            Output: Two distinct documents in [CV_START][CV_END] and [COVER_START][COVER_END].
            
            CV Rules: 
            - Use STAR method. No 'Expert' levels.
            - Format: Professional, +212 Phone, Casablanca Location.
            
            Cover Letter Rules:
            - Professional header. Tailored to {dest} business culture.
            - Focus on results and achievements.
            """
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt + "\nData: " + raw_text}],
                temperature=0.1
            )
            data = res.choices[0].message.content
            st.session_state.final_cv = data.split("[CV_START]")[1].split("[CV_END]")[0].strip()
            st.session_state.final_cover = data.split("[COVER_START]")[1].split("[COVER_END]")[0].strip()
        except: st.error("Parsing Error. Try again.")

# --- Results (Separation View) ---
if 'final_cv' in st.session_state:
    st.write("---")
    col_cv, col_cover = st.columns(2)
    
    with col_cv:
        st.subheader("📄 Professional CV")
        st.markdown(f"<div class='card'>{st.session_state.final_cv}</div>", unsafe_allow_html=True)
        pdf_cv = build_pdf(st.session_state.final_cv, "Curriculum Vitae", dest)
        st.download_button("📥 Download CV (PDF)", pdf_cv, "CV_Pro.pdf", "application/pdf")

    with col_cover:
        st.subheader("✉️ Cover Letter")
        st.markdown(f"<div class='card'>{st.session_state.final_cover}</div>", unsafe_allow_html=True)
        pdf_cover = build_pdf(st.session_state.final_cover, "Cover Letter", dest)
        st.download_button("📥 Download Letter (PDF)", pdf_cover, "Cover_Letter.pdf", "application/pdf")
