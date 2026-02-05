import streamlit as st
from groq import Groq
import streamlit.components.v1 as components
from PyPDF2 import PdfReader
import docx2txt

# 1. Config dyal l-page
st.set_page_config(page_title="Global Resume Pro", page_icon="🇪🇺", layout="wide")

# 2. CSS Style (Standard Fonts for ATS)
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
    .stApp { background-color: #F8F9FA; }
    .doc-preview {
        background-color: white; padding: 40px 50px; margin: auto;
        color: #000 !important; font-family: 'Arial', sans-serif;
        line-height: 1.5; border: 1px solid #DDD; max-width: 800px;
    }
    .stButton>button { width: 100%; border-radius: 6px; font-weight: bold; background-color: #2D3E50; color: white; }
    </style>
    """, unsafe_allow_html=True)

def get_text_from_file(file):
    try:
        if file.type == "application/pdf":
            return " ".join([p.extract_text() for p in PdfReader(file).pages])
        return docx2txt.process(file)
    except: return ""

# 3. Sidebar
with st.sidebar:
    st.title("🌍 Market Selector")
    api_key = st.text_input("Groq API Key", type="password")
    market = st.selectbox("Select Target Region", ["Europe (Professional/Europass)", "Canada (Achievement-Based)"])
    st.divider()
    st.info("⚠️ Ensure requirements.txt includes: streamlit, groq, PyPDF2, docx2txt")

# 4. Inputs Section
st.title("CV & Cover Letter Multi-Region Optimizer")
c1, c2 = st.columns([1, 1], gap="large")

with c1:
    st.subheader("📤 Source Material")
    up_file = st.file_uploader("Upload Current CV", type=["pdf", "docx"])
    manual_text = st.text_area("Or Paste Text:", height=200)
    input_data = get_text_from_file(up_file) if up_file else manual_text

with c2:
    st.subheader("🎯 Personal & Professional Info")
    job_target = st.text_input("Target Job Title", value="Digital Marketing Specialist")
    citizenship = st.text_input("Citizenship", placeholder="e.g. Moroccan")
    work_permit = st.text_input("Work Permit / Visa Status", placeholder="e.g. Valid Work Permit / Sponsorship Required")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        eng_lvl = st.selectbox("English", ["Full Professional", "Bilingual", "Native"])
    with col_l2:
        fr_lvl = st.selectbox("French", ["Professional Working", "Full Professional", "Native"])

    generate_btn = st.button("🚀 Build My Global Package")

# 5. The AI Intelligence
if generate_btn:
    if not api_key: st.error("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")
    elif not input_data: st.warning("CV content is empty!")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner(f"Restructuring for {market}..."):
                
                # Market-specific logic
                is_europe = "Europe" in market
                style_rules = f"""
                1. HEADER: Include Citizenship: {citizenship} and Work Permit: {work_permit}.
                2. SUMMARY: 100% Reality-based. Experience + Key Industry Skills.
                3. EXPERIENCE: {'Add the Industry/Context for each company (e.g. IT Services, Retail).' if is_europe else 'Focus on STAR method & Annualized budgets.'}
                4. SKILLS: Add a 'Soft Skills' section with: Adaptability, Teamwork, Intercultural Communication.
                5. CERTIFICATIONS: Create a dedicated section for professional certifications.
                6. LANGUAGES: English ({eng_lvl}), French ({fr_lvl}).
                """

                # CV Generation
                cv_p = f"Rewrite this CV for {job_target} in {market}. Rules: {style_rules}. CV Data: {input_data}"
                cv_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":cv_p}])
                st.session_state['final_cv'] = cv_res.choices[0].message.content

                # Letter Generation
                cl_p = f"Write a professional Cover Letter for {job_target} for the {market} market. Match the CV achievements and context: {input_data}"
                cl_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":cl_p}])
                st.session_state['final_cl'] = cl_res.choices[0].message.content
                
                st.balloons()
        except Exception as e: st.error(f"Error: {e}")

# 6. Optimized PDF Download (FIXED)
def pdf_button(area_id, filename):
    components.html(f"""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
        <button onclick="downloadPDF()" style="width:100%; height:40px; background-color:#27ae60; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">
            📥 Download {filename}
        </button>
        <script>
        function downloadPDF() {{
            var element = window.parent.document.getElementById('{area_id}');
            var opt = {{ margin: 10, filename: '{filename}', html2canvas: {{ scale: 2 }}, jsPDF: {{ format: 'a4' }} }};
            html2pdf().from(element).set(opt).save();
        }}
        </script>""", height=50)

if 'final_cv' in st.session_state:
    st.divider()
    t_cv, t_cl = st.tabs(["📄 Optimized CV", "✉️ Cover Letter"])
    
    with t_cv:
        cv_clean = st.session_state['final_cv'].replace("\n", "<br>").replace("**", "<b>")
        st.markdown(f'<div id="cv_view" class="doc-preview">{cv_clean}</div>', unsafe_allow_html=True)
        pdf_button("cv_view", f"CV_{job_target.replace(' ', '_')}.pdf")

    with t_cl:
        cl_clean = st.session_state['final_cl'].replace("\n", "<br>").replace("**", "<b>")
        st.markdown(f'<div id="cl_view" class="doc-preview">{cl_clean}</div>', unsafe_allow_html=True)
        pdf_button("cl_view", f"CoverLetter_{job_target.replace(' ', '_')}.pdf")
