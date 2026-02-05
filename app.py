import streamlit as st
from groq import Groq
import streamlit.components.v1 as components
from PyPDF2 import PdfReader
import docx2txt

# 1. Page Config
st.set_page_config(page_title="Career Pro: CV & Letter", page_icon="💼", layout="wide")

# 2. CSS Style (Standard Fonts for ATS)
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
    .stApp { background-color: #F9FAFB; }
    .doc-preview {
        background-color: white; padding: 60px; margin: 20px auto;
        color: #000 !important; font-family: 'Times New Roman', serif;
        line-height: 1.6; border: 1px solid #DDD; max-width: 800px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .stButton>button { width: 100%; border-radius: 6px; font-weight: bold; background-color: #C53030; color: white; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# Function to extract text from files
def get_text_from_upload(file):
    try:
        if file.type == "application/pdf":
            return " ".join([p.extract_text() for p in PdfReader(file).pages])
        return docx2txt.process(file)
    except Exception as e:
        return f"Error: {e}"

# 3. Sidebar
with st.sidebar:
    st.title("🚀 Career Engine")
    api_key = st.text_input("Groq API Key", type="password")
    market = st.selectbox("Target Market", ["Canada (Achievement Focus)", "Europe (Structured/Modern)"])
    st.info("Don't forget to create requirements.txt with: streamlit, groq, PyPDF2, docx2txt")

# 4. Input Section
st.title("CV & Cover Letter Pro Optimizer")
c1, c2 = st.columns([1.2, 1], gap="large")

with c1:
    st.subheader("📤 Source Materials")
    up_file = st.file_uploader("Upload your CV (PDF/DOCX)", type=["pdf", "docx"])
    manual_cv = st.text_area("Or paste text here:", height=200)
    input_text = get_text_from_upload(up_file) if up_file else manual_cv

with c2:
    st.subheader("🎯 Optimization Settings")
    target_job = st.text_input("Target Job Title", value="Digital Marketing Specialist")
    
    # Automatic professional leveling for ENCG profile
    eng_lvl = st.selectbox("English Level", ["Full Professional Proficiency", "Bilingual", "Native"])
    fr_lvl = st.selectbox("French Level", ["Professional Working Proficiency", "Full Professional", "Native"])
    
    generate_all = st.button("🔥 Generate Pro CV & Cover Letter")

# 5. The AI Processing
if generate_all:
    if not api_key: st.error("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")
    elif not input_text: st.warning("Please provide your CV content")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner("Writing your professional documents..."):
                
                # Rule logic for high competition markets
                sys_rules = f"""
                1. No emotional fluff. Professional and direct.
                2. Use Action Verbs (Spearheaded, Orchestrated, Administered).
                3. Annualize budgets (e.g., $5,000 monthly -> $60,000 Annual budget).
                4. Languages: English ({eng_lvl}), French ({fr_lvl}).
                5. Location: Focus on City, Country (no relocation mention).
                6. CV Structure: Professional Summary, Core Competencies, Experience, Education, Certifications, Languages.
                """

                # CV Generation
                cv_p = f"Rewrite this CV for {target_job} in {market}. Rules: {sys_rules}. CV Data: {input_text}"
                cv_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":cv_p}])
                st.session_state['cv_final'] = cv_res.choices[0].message.content

                # Cover Letter Generation (New Agent)
                cl_p = f"Write a professional and persuasive Cover Letter for {target_job} in {market}. Match the achievements mentioned in the CV: {input_text}. Be concise and high-impact."
                cl_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":cl_p}])
                st.session_state['cl_final'] = cl_res.choices[0].message.content
                
                st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")

# 6. Preview & Fixed Download Section
if 'cv_final' in st.session_state:
    st.write("---")
    tab_cv, tab_cl = st.tabs(["📄 Optimized Resume", "✉️ Professional Cover Letter"])
    
    with tab_cv:
        html_cv = st.session_state['cv_final'].replace("\n", "<br>").replace("**", "<b>")
        st.markdown(f'<div id="cv_box" class="doc-preview">{html_cv}</div>', unsafe_allow_html=True)
        if st.button("📥 Download CV (PDF)"):
            components.html(f"""
                <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
                <script>
                var opt = {{ margin: 10, filename: 'CV_Optimized.pdf', html2canvas: {{ scale: 2 }}, jsPDF: {{ format: 'a4' }} }};
                html2pdf().from(window.parent.document.getElementById('cv_box')).set(opt).save();
                </script>""", height=0)

    with tab_cl:
        html_cl = st.session_state['cl_final'].replace("\n", "<br>").replace("**", "<b>")
        st.markdown(f'<div id="cl_box" class="doc-preview">{html_cl}</div>', unsafe_allow_html=True)
        if st.button("📥 Download Cover Letter (PDF)"):
            components.html(f"""
                <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
                <script>
                var opt = {{ margin: 10, filename: 'Cover_Letter.pdf', html2canvas: {{ scale: 2 }}, jsPDF: {{ format: 'a4' }} }};
                html2pdf().from(window.parent.document.getElementById('cl_box')).set(opt).save();
                </script>""", height=0)
