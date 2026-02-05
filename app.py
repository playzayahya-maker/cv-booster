import streamlit as st
from groq import Groq
import streamlit.components.v1 as components
from PyPDF2 import PdfReader
import docx2txt

# 1. Page Config
st.set_page_config(page_title="Global Career Pro", page_icon="💼", layout="wide")

# 2. 🔑 Hardcoded API Key (Blast API Key hna nichan)
# Ghir bedel had l-khit b l-key dyalk l-real o 7mih f l-code
MY_GROQ_KEY = "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"

# 3. CSS Style (Executive Look)
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
    .stApp { background-color: #F8F9FA; }
    .doc-preview {
        background-color: white; padding: 50px; margin: auto;
        color: #000 !important; font-family: 'Times New Roman', serif;
        line-height: 1.6; border: 1px solid #DDD; max-width: 800px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stButton>button { width: 100%; border-radius: 6px; font-weight: bold; background-color: #1A365D; color: white; height: 3.2em; }
    </style>
    """, unsafe_allow_html=True)

def extract_text(file):
    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
        return docx2txt.process(file)
    except: return ""

# 4. Sidebar
with st.sidebar:
    st.title("🌍 Market Selector")
    market = st.selectbox("Select Target Region", ["Canada (Achievement/STAR)", "Europe (Visa/Context)"])
    st.divider()
    st.success("App Ready for Personal Use ✅")

# 5. Interface
st.title("CV & Cover Letter Pro Optimizer")
c1, c2 = st.columns([1.2, 1], gap="large")

with c1:
    st.subheader("📤 Source Materials")
    up_file = st.file_uploader("Upload CV (PDF/DOCX)", type=["pdf", "docx"])
    manual_text = st.text_area("Or Paste CV Content:", height=250)
    input_text = extract_text(up_file) if up_file else manual_text

with c2:
    st.subheader("🎯 Personal & Target Info")
    job_target = st.text_input("Target Job Title", value="Digital Marketing Specialist")
    citizenship = st.text_input("Citizenship", placeholder="e.g. Moroccan")
    visa_status = st.text_input("Work Permit Status", placeholder="e.g. Sponsorship Needed")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        eng = st.selectbox("English", ["Full Professional", "Bilingual", "Native"])
    with col_l2:
        fr = st.selectbox("French", ["Professional Working", "Full Professional", "Native"])
    
    certs = st.text_input("Certifications", placeholder="Google, Meta, etc.")
    generate_btn = st.button("🚀 GENERATE FULL CAREER PACKAGE")

# 6. AI Engine
if generate_btn:
    if not input_text:
        st.warning("Please provide your CV content.")
    elif MY_GROQ_KEY == "ADD_YOUR_GROQ_API_KEY_HERE":
        st.error("⚠️ Nta nssiti ma-bedeltich l-API Key wast l-code!")
    else:
        try:
            client = Groq(api_key=MY_GROQ_KEY)
            with st.spinner(f"Engineering for {market}..."):
                is_europe = "Europe" in market
                rules = f"""
                - HEADER: Include Citizenship: {citizenship} and Work Permit: {visa_status}.
                - SUMMARY: Results-driven, no emotional fluff.
                - EXPERIENCE: {'Add Industry Context (e.g. Fintech) for each company.' if is_europe else 'Strictly use STAR method & Annualized metrics.'}
                - SKILLS: Add Adaptability, Teamwork, Intercultural Communication.
                - LANGUAGES: English ({eng}), French ({fr}).
                - CERTIFICATIONS: Include {certs}.
                """

                # CV Generation
                cv_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Rewrite CV for {job_target} in {market}. Rules: {rules}. Data: {input_text}"}]
                )
                st.session_state['cv_final'] = cv_res.choices[0].message.content

                # Letter Generation
                cl_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Write a professional Cover Letter for {job_target} for {market} based on: {input_text}."}]
                )
                st.session_state['cl_final'] = cl_res.choices[0].message.content
                st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")

# 7. Download Component (Universal Fix)
def pdf_button(area_id, filename):
    components.html(f"""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
        <button onclick="dl()" style="width:100%; height:45px; background-color:#27ae60; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">
            📥 Download {filename}
        </button>
        <script>
        function dl() {{
            const el = window.parent.document.getElementById('{area_id}');
            html2pdf().from(el).set({{ margin: 10, filename: '{filename}', html2canvas: {{ scale: 2 }}, jsPDF: {{ format: 'a4' }} }}).save();
        }}
        </script>""", height=60)

if 'cv_final' in st.session_state:
    st.divider()
    # Explicitly using clear tab names to prevent NameErrors
    tab_resume, tab_letter = st.tabs(["📄 Optimized Resume", "✉️ Cover Letter"])
    
    with tab_resume:
        cv_h = st.session_state['cv_final'].replace("\n", "<br>").replace("**", "<b>")
        st.markdown(f'<div id="cv_o" class="doc-preview">{cv_h}</div>', unsafe_allow_html=True)
        pdf_button("cv_o", "Optimized_CV.pdf")

    with tab_letter:
        cl_h = st.session_state['cl_final'].replace("\n", "<br>").replace("**", "<b>")
        st.markdown(f'<div id="cl_o" class="doc-preview">{cl_h}</div>', unsafe_allow_html=True)
        pdf_button("cl_o", "Cover_Letter.pdf")
        
