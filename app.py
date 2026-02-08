import streamlit as st
from groq import Groq
import pdfplumber
from fpdf import FPDF

# --- UI STYLE ---
st.set_page_config(page_title="Architect Pro V31", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #fcfaff; }
    .stButton>button { background: #6d28d9; color: white; border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

class ProfessionalCV(FPDF):
    def add_sidebar(self):
        self.set_fill_color(109, 40, 217) # Mauve
        self.rect(0, 0, 10, 297, 'F') # Thin sidebar for style

    def draw_header(self, name, title, contact):
        self.set_font("Helvetica", 'B', 24)
        self.set_text_color(109, 40, 217)
        self.cell(0, 15, name.upper(), ln=True)
        self.set_font("Helvetica", 'I', 14)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, title, ln=True)
        self.set_font("Helvetica", '', 9)
        self.set_text_color(50, 50, 50)
        self.cell(0, 5, contact, ln=True)
        self.ln(10)

    def draw_section(self, title):
        self.set_font("Helvetica", 'B', 12)
        self.set_text_color(109, 40, 217)
        self.cell(0, 10, title.upper(), ln=True)
        self.set_draw_color(109, 40, 217)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(5)

def generate_designer_pdf(content, market, is_cv=True):
    pdf = ProfessionalCV()
    pdf.add_page()
    pdf.add_sidebar()
    
    # Simple Parsing
    lines = content.split('\n')
    name = lines[0] if lines else "Amine El Idrissi"
    contact = "Casablanca, Morocco | +212 555-123-4567 | email@domain.com"
    
    if is_cv:
        pdf.draw_header(name, "Data Analyst", contact)
        # Formating the content into sections
        pdf.set_font("Helvetica", '', 10)
        pdf.set_text_color(0, 0, 0)
        clean_text = content.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 6, clean_text)
    else:
        # Cover Letter Style
        pdf.draw_header(name, "Cover Letter", contact)
        pdf.ln(10)
        pdf.set_font("Helvetica", '', 11)
        pdf.multi_cell(0, 7, content.encode('latin-1', 'ignore').decode('latin-1'))
        
    return bytes(pdf.output())

# --- APP LOGIC ---
st.title("✨ Elite CV & Cover Letter Designer")

with st.sidebar:
    api_key = st.text_input("Groq API Key:", type="password")
    market = st.selectbox("Market:", ["Canada", "Europe (France/Germany)"])

t1, t2 = st.tabs(["📤 Upload PDF", "✍️ Paste Text"])
user_input = ""
if t1.file_uploader("Upload", type=['pdf'], label_visibility="collapsed", key="pdf"):
    with pdfplumber.open(st.session_state.pdf) as p:
        user_input = "\n".join([page.extract_text() for page in p.pages if page.extract_text()])
if t2.text_area("Content", height=200, label_visibility="collapsed", key="txt"):
    user_input = st.session_state.txt

if st.button("DESIGN MY DOCUMENTS →"):
    if api_key and user_input:
        client = Groq(api_key=api_key)
        prompt = f"Create a professional CV and a matching Cover Letter for {market}. Separate with [CV] and [LETTER]. Use STAR method and metrics."
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt + "\n" + user_input}])
        raw = res.choices[0].message.content
        st.session_state.cv_out = raw.split("[CV]")[1].split("[LETTER]")[0].strip()
        st.session_state.lt_out = raw.split("[LETTER]")[1].strip()

# --- RESULTS ---
if 'cv_out' in st.session_state:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📄 Designer CV")
        st.download_button("📥 Download Styled CV", generate_designer_pdf(st.session_state.cv_out, market, True), "CV_Designer.pdf")
        st.markdown(f"<div style='background:white; padding:20px; border-left:10px solid #6d28d9;'>{st.session_state.cv_out}</div>", unsafe_allow_html=True)
    with c2:
        st.subheader("✉️ Pro Cover Letter")
        st.download_button("📥 Download Styled Letter", generate_designer_pdf(st.session_state.lt_out, market, False), "Letter_Designer.pdf")
        st.markdown(f"<div style='background:white; padding:20px; border-top:10px solid #6d28d9;'>{st.session_state.lt_out}</div>", unsafe_allow_html=True)
