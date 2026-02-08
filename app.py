import streamlit as st
from groq import Groq
import pdfplumber
from fpdf import FPDF

# --- UI APP ---
st.set_page_config(page_title="Elite CV Designer", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .preview-card { background: white; padding: 25px; border-radius: 12px; border-top: 8px solid #6d28d9; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .stButton>button { background: #6d28d9; color: white; border-radius: 10px; font-weight: bold; height: 50px; }
</style>
""", unsafe_allow_html=True)

# --- CLASS PDF L-MZOWQA ---
class ElitePDF(FPDF):
    def header_pro(self, name, title, contact):
        # Header Mauve b7al s-tsawer
        self.set_fill_color(109, 40, 217) 
        self.rect(0, 0, 210, 50, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", 'B', 26)
        self.set_xy(15, 12)
        self.cell(0, 10, name.upper(), ln=True)
        self.set_font("Helvetica", '', 14)
        self.cell(0, 10, title, ln=True)
        self.set_font("Helvetica", '', 9)
        self.set_xy(15, 32)
        self.multi_cell(0, 5, contact)
        self.ln(25)

    def draw_section(self, label):
        self.ln(5)
        self.set_font("Helvetica", 'B', 12)
        self.set_text_color(109, 40, 217)
        self.cell(0, 10, label.upper(), ln=True)
        self.set_draw_color(109, 40, 217)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y()) # Line b7al Screenshot 233
        self.ln(3)

def generate_styled_doc(text, doc_type, market):
    pdf = ElitePDF()
    pdf.add_page()
    
    # Separation d l-content
    lines = text.split('\n')
    name = lines[0] if lines else "Amine El Idrissi"
    contact = "Casablanca, Morocco | +212 661-000000 | amine@email.com"
    
    # Drawing Header
    pdf.header_pro(name, "DATA ANALYST" if doc_type == "CV" else "COVER LETTER", contact)
    
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Helvetica", '', 10)
    
    # Encoding fix dial Screenshot 291
    safe_text = text.encode('latin-1', 'ignore').decode('latin-1')
    
    if doc_type == "CV":
        # Sections simulation b7al s-tsawer
        sections = ["Professional Summary", "Experience", "Technical Skills", "Education"]
        for sec in sections:
            pdf.draw_section(sec)
            pdf.multi_cell(0, 6, "Key achievements and professional details based on the AI output...")
            pdf.ln(2)
        # Full content below (bach mat-t-tweddarch l-m3loumat)
        pdf.add_page()
        pdf.draw_section("Full Detailed Output")
        pdf.multi_cell(0, 5, safe_text)
    else:
        pdf.draw_section("Motivation & Application")
        pdf.set_font("Helvetica", '', 11)
        pdf.multi_cell(0, 7, safe_text)
        
    return bytes(pdf.output())

# --- INTERFACE ---
st.title("💎 CV Booster Premium V33")

with st.sidebar:
    api_key = st.text_input("Groq API Key:", type="password")
    market = st.selectbox("Market:", ["Canada", "France", "UK"])

t1, t2 = st.tabs(["📤 Subir Archivo", "✍️ Pegar Texto"])
user_input = ""
if t1.file_uploader("Upload", type=['pdf'], label_visibility="collapsed", key="u"):
    with pdfplumber.open(st.session_state.u) as p:
        user_input = "\n".join([page.extract_text() for page in p.pages if page.extract_text()])
if t2.text_area("Paste", height=200, label_visibility="collapsed", key="p"):
    user_input = st.session_state.p

if st.button("DESIGN & GENERATE MY ELITE PACK"):
    if api_key and user_input:
        client = Groq(api_key=api_key)
        prompt = f"Expert {market} CV/Cover Letter. Use [CV] and [LETTER] tags. STAR method."
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt + "\n" + user_input}])
        raw = res.choices[0].message.content
        st.session_state.cv_final = raw.split("[CV]")[1].split("[LETTER]")[0].strip()
        st.session_state.lt_final = raw.split("[LETTER]")[1].strip()

# --- RESULTS ---
if 'cv_final' in st.session_state:
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📄 Elite CV")
        st.markdown(f"<div class='preview-card'>{st.session_state.cv_final}</div>", unsafe_allow_html=True)
        st.download_button("📥 Download Styled CV", generate_styled_doc(st.session_state.cv_final, "CV", market), "CV_Elite.pdf")
    with c2:
        st.subheader("✉️ Pro Cover Letter")
        st.markdown(f"<div class='preview-card'>{st.session_state.lt_final}</div>", unsafe_allow_html=True)
        st.download_button("📥 Download Styled Letter", generate_styled_doc(st.session_state.lt_final, "LETTER", market), "Letter_Elite.pdf")
