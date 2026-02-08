import streamlit as st
from groq import Groq
import pdfplumber
from fpdf import FPDF

# --- UI STYLE B7AL L-PHOTO ---
st.set_page_config(page_title="CV Booster Elite", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #fcfaff; }
    .preview-card { background: white; padding: 25px; border-radius: 12px; border-top: 6px solid #6d28d9; box-shadow: 0 4px 20px rgba(0,0,0,0.08); font-family: 'Helvetica'; }
    .stButton>button { background: #6d28d9; color: white; border-radius: 10px; font-weight: bold; height: 50px; }
</style>
""", unsafe_allow_html=True)

# --- CLASS PDF M-ZOWQA ---
class StyledPDF(FPDF):
    def draw_header(self, name, contact):
        self.set_fill_color(109, 40, 217) # Mauve
        self.rect(0, 0, 210, 45, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", 'B', 24)
        self.set_xy(15, 12)
        self.cell(0, 10, name.upper(), ln=True)
        self.set_font("Helvetica", '', 10)
        self.set_xy(15, 25)
        self.multi_cell(0, 5, contact)
        self.ln(20)

    def draw_section_header(self, title):
        self.ln(5)
        self.set_font("Helvetica", 'B', 13)
        self.set_text_color(109, 40, 217)
        self.cell(0, 10, title.upper(), ln=True)
        self.set_draw_color(109, 40, 217)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

def generate_elite_pdf(text, doc_type, market):
    pdf = StyledPDF()
    pdf.add_page()
    
    # Parsing simple dial s-smiya o l-contact
    lines = text.split('\n')
    name = lines[0] if lines else "AMINE EL IDRISSI"
    contact = "Casablanca, Morocco | +212 555-123456 | linkedin.com/in/amine"

    pdf.draw_header(name, contact)
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Helvetica", '', 10)
    
    # Fix dial l-encoding
    safe_text = text.encode('latin-1', 'ignore').decode('latin-1')
    
    if doc_type == "CV":
        # Hna l-AI ghadi i-ktb s-text, o l-code t-i-7to m-formati
        pdf.multi_cell(0, 6, safe_text)
    else:
        pdf.draw_section_header("COVER LETTER")
        pdf.set_font("Helvetica", '', 11)
        pdf.multi_cell(0, 7, safe_text)
        
    return bytes(pdf.output())

# --- INTERFACE ---
st.title("🚀 CV & Cover Letter Elite Architect")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Groq API Key:", type="password")
    market = st.selectbox("Target Country:", ["Canada", "France", "Germany", "UK"])

# Tabs b7al s-tsawer dialk
t1, t2 = st.tabs(["📤 Upload PDF", "✍️ Paste Text"])
user_data = ""
with t1:
    f = st.file_uploader("Upload CV", type=['pdf'], label_visibility="collapsed")
    if f:
        with pdfplumber.open(f) as p:
            user_data = "\n".join([page.extract_text() for page in p.pages if page.extract_text()])
with t2:
    txt = st.text_area("Paste CV content", height=200, label_visibility="collapsed")
    if txt: user_data = txt

# --- GENERATION ---
if st.button("DESIGN & GENERATE MY PACK →"):
    if api_key and user_data:
        try:
            client = Groq(api_key=api_key)
            prompt = f"Create a professional CV and Cover Letter for {market}. Use STAR method. Separate with [CV_ELITE] and [COVER_ELITE]."
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt + "\n" + user_data}]
            )
            raw = res.choices[0].message.content
            st.session_state.final_cv = raw.split("[CV_ELITE]")[1].split("[COVER_ELITE]")[0].strip()
            st.session_state.final_cover = raw.split("[COVER_ELITE]")[1].strip()
        except: st.error("Format Error. Please try again.")

# --- RESULTS DISPLAY ---
if 'final_cv' in st.session_state:
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Professional CV")
        st.markdown(f"<div class='preview-card'>{st.session_state.final_cv}</div>", unsafe_allow_html=True)
        # Fix dial l-download bytes
        cv_bytes = generate_elite_pdf(st.session_state.final_cv, "CV", market)
        st.download_button("📥 Download Styled CV", cv_bytes, "CV_Elite.pdf")

    with col2:
        st.subheader("✉️ Pro Cover Letter")
        st.markdown(f"<div class='preview-card'>{st.session_state.final_cover}</div>", unsafe_allow_html=True)
        cover_bytes = generate_elite_pdf(st.session_state.final_cover, "LETTER", market)
        st.download_button("📥 Download Styled Letter", cover_bytes, "Letter_Elite.pdf")
