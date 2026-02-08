import streamlit as st
from groq import Groq
import pdfplumber
from fpdf import FPDF

# --- CONFIGURATION VISUELLE ---
st.set_page_config(page_title="CV Booster Pro", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #f4f7fe; }
    .preview-box { background: white; padding: 25px; border-radius: 10px; border-top: 5px solid #6d28d9; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); font-family: 'Segoe UI'; }
    .stButton>button { background: linear-gradient(90deg, #6d28d9 0%, #4f46e5 100%); color: white; font-weight: bold; border: none; height: 50px; }
</style>
""", unsafe_allow_html=True)

# --- ENGINE DIAL L-ALWAN O FORMATION ---
class StyledPDF(FPDF):
    def header_styled(self, name, title, contact_info):
        self.set_fill_color(109, 40, 217) # Mauve
        self.rect(0, 0, 210, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 22)
        self.set_xy(10, 10)
        self.cell(0, 10, name.upper(), ln=True)
        self.set_font("Arial", '', 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", '', 9)
        self.cell(0, 5, contact_info, ln=True)
        self.ln(15)

    def section_title(self, label):
        self.set_font("Arial", 'B', 12)
        self.set_text_color(109, 40, 217)
        self.cell(0, 10, label.upper(), ln=True)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

def generate_pro_pdf(text, type_doc, market):
    pdf = StyledPDF()
    pdf.add_page()
    
    # Extraction dyal s-smiya o title (Simplified for test)
    lines = text.split('\n')
    name = lines[0] if len(lines) > 0 else "Full Name"
    contact = "Casablanca, Morocco | +212 600-000000 | email@example.com"
    
    if type_doc == "CV":
        pdf.header_styled(name, "Professional Profile", contact)
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Arial", size=10)
        # Hna n-formatiw l-body (Simple logic for demo)
        safe_text = text.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 6, safe_text)
    else:
        # Cover Letter style
        pdf.header_styled(name, "Cover Letter", contact)
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Arial", size=11)
        pdf.ln(10)
        safe_text = text.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 7, safe_text)
        
    return bytes(pdf.output())

# --- INTERFACE ---
st.title("🚀 CV & Cover Letter - High Professional")

with st.sidebar:
    key = st.text_input("Groq API Key:", type="password")
    dest = st.selectbox("Market:", ["Canada", "France", "Germany"])

# Inputs
t1, t2 = st.tabs(["📤 Subir Archivo", "✍️ Pegar Texto"])
raw_input = ""
with t1:
    f = st.file_uploader("Upload PDF", type=['pdf'], label_visibility="collapsed")
    if f:
        with pdfplumber.open(f) as p:
            raw_input = "\n".join([page.extract_text() for page in p.pages if page.extract_text()])
with t2:
    txt = st.text_area("Paste here", height=200, label_visibility="collapsed")
    if txt: raw_input = txt

if st.button("GENERATE PRO DOCUMENTS"):
    if key and raw_input:
        client = Groq(api_key=key)
        prompt = f"Create a professional CV and a matching Cover Letter for {dest}. Split with [CV] and [LETTER]. Use STAR method."
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt + "\n" + raw_input}]
        )
        content = res.choices[0].message.content
        st.session_state.cv_p = content.split("[CV]")[1].split("[LETTER]")[0].strip()
        st.session_state.lt_p = content.split("[LETTER]")[1].strip()

# --- DISPLAY ---
if 'cv_p' in st.session_state:
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📄 Professional CV")
        st.markdown(f"<div class='preview-box'>{st.session_state.cv_p}</div>", unsafe_allow_html=True)
        cv_b = generate_pro_pdf(st.session_state.cv_p, "CV", dest)
        st.download_button("📥 Download CV", cv_b, "CV_Pro.pdf")
    with c2:
        st.subheader("✉️ Cover Letter")
        st.markdown(f"<div class='preview-box'>{st.session_state.lt_p}</div>", unsafe_allow_html=True)
        lt_b = generate_pro_pdf(st.session_state.lt_p, "LETTER", dest)
        st.download_button("📥 Download Letter", lt_b, "Letter_Pro.pdf")
