import streamlit as st
from groq import Groq
import pdfplumber
from fpdf import FPDF

# --- UI SETUP ---
st.set_page_config(page_title="CV & Cover Pro", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #fcfaff; }
    .doc-box { background: white; padding: 25px; border-radius: 8px; border: 1px solid #ddd; height: 500px; overflow-y: auto; color: #333; }
    .stButton>button { background: #6d28d9; color: white; width: 100%; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- SAFE PDF ENGINE ---
def make_pdf(text, title, market):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, title.upper(), ln=True, align='L' if market == "Canada" else 'C')
    pdf.line(10, 22, 200, 22)
    pdf.ln(10)
    pdf.set_font("Helvetica", size=10)
    # Fix for Screenshot 288/291: Encode to latin-1 but ignore errors
    safe_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 6, safe_text)
    return pdf.output()

# --- EXTRACTION ---
def extract_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

st.title("🚀 CV & Cover Letter Architect")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Groq API Key:", type="password")
    market = st.selectbox("Target Country:", ["Canada", "Germany", "France", "UK", "Spain", "Italy"])

# --- INPUTS ---
t1, t2 = st.tabs(["📤 Upload PDF CV", "✍️ Paste Content"])
input_data = ""
with t1:
    up = st.file_uploader("Drop CV here", type=['pdf'], label_visibility="collapsed")
    if up: input_data = extract_pdf(up)
with t2:
    txt = st.text_area("Or paste experience", height=200, label_visibility="collapsed")
    if txt: input_data += "\n" + txt

# --- ACTION ---
if st.button("GENERATE BOTH DOCUMENTS"):
    if not api_key or not input_data:
        st.error("Missing API Key or CV Data.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI is thinking..."):
                # One prompt for both to ensure context, but very clear separators
                prompt = f"Create a professional CV and a matching Cover Letter for {market}. Use STAR method. Use [CV_SECTION] and [COVER_SECTION] to separate them."
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"{prompt}\nData: {input_data}"}],
                    temperature=0.1
                )
                full_res = res.choices[0].message.content
                
                # Parsing logic to ensure cover is not lost
                if "[CV_SECTION]" in full_res and "[COVER_SECTION]" in full_res:
                    st.session_state.cv = full_res.split("[CV_SECTION]")[1].split("[COVER_SECTION]")[0].strip()
                    st.session_state.cover = full_res.split("[COVER_SECTION]")[1].strip()
                else:
                    st.error("AI Response format issue. Please try again.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- FINAL DISPLAY (CV & COVER INDEPENDENT) ---
if 'cv' in st.session_state and 'cover' in st.session_state:
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Optimized CV")
        st.markdown(f"<div class='doc-box'>{st.session_state.cv}</div>", unsafe_allow_html=True)
        cv_bytes = make_pdf(st.session_state.cv, "Curriculum Vitae", market)
        st.download_button("📥 Download CV", cv_bytes, "Professional_CV.pdf")

    with col2:
        st.subheader("✉️ Cover Letter")
        st.markdown(f"<div class='doc-box'>{st.session_state.cover}</div>", unsafe_allow_html=True)
        cover_bytes = make_pdf(st.session_state.cover, "Cover Letter", market)
        st.download_button("📥 Download Letter", cover_bytes, "Motivation_Letter.pdf")
