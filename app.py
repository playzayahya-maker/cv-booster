import streamlit as st
from groq import Groq
import streamlit.components.v1 as components
from PyPDF2 import PdfReader
import docx2txt

# 1. Page Config
st.set_page_config(page_title="Global Career Pro", page_icon="💼", layout="wide")

# 2. CSS Style (Clean & Professional for ATS compatibility)
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
    .stApp { background-color: #F4F7F9; }
    .doc-preview {
        background-color: white; padding: 45px 55px; margin: auto;
        color: #000 !important; font-family: 'Arial', sans-serif;
        line-height: 1.5; border: 1px solid #DDD; max-width: 800px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .stButton>button { width: 100%; border-radius: 4px; font-weight: bold; background-color: #1A365D; color: white; height: 3.2em; }
    .download-btn-style {
        background-color: #27ae60 !important; color: white !important; font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper: Extract text reliably
def get_text_from_file(file):
    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return docx2txt.process(file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
    return ""

# 3. Sidebar
with st.sidebar:
    st.title("⚙️ Career Settings")
    api_key = st.text_input("🔑 Groq API Key", type="password")
    market = st.selectbox("🌍 Target Region", ["Canada (Achievement/Metrics Focus)", "Europe (Context/Skills/Visa Focus)"])
    st.divider()
    st.success("ATS Standards Applied ✅")

# 4. Input Section
st.title("Professional Resume & Cover Letter Package")
c1, c2 = st.columns([1.2, 1], gap="large")

with c1:
    st.subheader("📤 Source Materials")
    up_file = st.file_uploader("Upload CV (PDF or DOCX)", type=["pdf", "docx"])
    manual_text = st.text_area("Or Paste Content Manually:", height=250, placeholder="Paste your current CV here...")
    
    # Process text
    input_text = ""
    if up_file:
        input_text = get_text_from_file(up_file)
        if input_text: st.toast("File Read Successfully!", icon='✅')
    else:
        input_text = manual_text

with c2:
    st.subheader("🎯 Optimization Details")
    job_target = st.text_input("Target Job Title", value="Digital Marketing Specialist")
    citizenship = st.text_input("Citizenship", placeholder="Moroccan")
    work_permit = st.text_input("Visa/Work Permit Status", placeholder="e.g. Valid Permit / Needs Sponsorship")
    
    cl1, cl2 = st.columns(2)
    with cl1:
        eng = st.selectbox("English Level", ["Full Professional Proficiency", "Bilingual", "Native"])
    with cl2:
        fr = st.selectbox("French Level", ["Professional Working Proficiency", "Full Professional", "Native"])
    
    certs = st.text_input("Certifications (Google, Meta, etc.)", placeholder="Add keywords for your certs")
    generate_btn = st.button("🚀 BUILD MY PROFESSIONAL PACKAGE")

# 5. The AI Logic
if generate_btn:
    if not api_key: st.error("Please enter your API Key in the sidebar.")
    elif not input_text: st.warning("Please provide your CV content first.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner(f"Optimizing for {market}..."):
                is_europe = "Europe" in market
                
                # Logic Injection
                style_prompt = f"""
                1. HEADER: Must include Citizenship: {citizenship} and Work Permit Status: {work_permit}.
                2. SUMMARY: Results-driven only. Start with: '{job_target} with X years of experience...'
                3. EXPERIENCE: {'Include Industry Context (e.g. Fintech, SaaS) for each role.' if is_europe else 'Strictly use STAR method with Annualized Metrics (e.g. Administered $60K/year budget).'}
                4. ACTION VERBS: Spearheaded, Orchestrated, Executed, Optimized.
                5. SKILLS: Include Adaptability, Teamwork, and Intercultural Communication.
                6. LANGUAGES: English ({eng}), French ({fr}).
                7. CERTIFICATIONS: Create a dedicated section for {certs}.
                """

                # Generate CV
                cv_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are a Senior Career Coach."},
                              {"role": "user", "content": f"Rewrite this CV for {job_target} in {market}. Rules: {style_prompt}. Content: {input_text}"}],
                    temperature=0.3
                )
                st.session_state['cv_final'] = cv_res.choices[0].message.content

                # Generate Letter
                cl_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are an Executive Recruiter."},
                              {"role": "user", "content": f"Write a high-impact Cover Letter for {job_target} in {market} based on: {input_text}."}],
                    temperature=0.4
                )
                st.session_state['cl_final'] = cl_res.choices[0].message.content
                st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")

# 6. Result & Universal Download Fix
def download_button(html_id, filename):
    components.html(f"""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
        <button onclick="generatePDF()" style="width:100%; height:50px; background-color:#27ae60; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold; font-size:16px;">
            📥 Download {filename} (PDF)
        </button>
        <script>
        function generatePDF() {{
            const element = window.parent.document.getElementById('{html_id}');
            const opt = {{
                margin: 15,
                filename: '{filename}',
                image: {{ type: 'jpeg', quality: 0.98 }},
                html2canvas: {{ scale: 2, useCORS: true }},
                jsPDF: {{ unit: 'mm', format: 'a4', orientation: 'portrait' }}
            }};
            html2pdf().from(element).set(opt).save();
        }}
        </script>""", height=70)

if 'cv_final' in st.session_state:
    st.divider()
    t1, t2 = st.tabs(["📄 Optimized Resume", "✉️ Tailored Cover Letter"])
    
    with t1:
        cv_disp = st.session_state['cv_final'].replace("\n", "<br>").replace("**", "<b>")
        st.markdown(f'<div id="cv_print" class="doc-preview">{cv_disp}</div>', unsafe_allow_html=True)
        download_button("cv_print", f"Resume_{job_target.replace(' ', '_')}.pdf")

    with t2:
        cl_disp = st.session_state['cl_final'].replace("\n", "<br>").replace("**", "<b>")
        st.markdown(f'<div id="cl_print" class="doc-preview">{cl_disp}</div>', unsafe_allow_html=True)
        download_button("cl_print", f"CoverLetter_{job_target.replace(' ', '_')}.pdf")

    with t_cl:
        cl_clean = st.session_state['final_cl'].replace("\n", "<br>").replace("**", "<b>")
        st.markdown(f'<div id="cl_view" class="doc-preview">{cl_clean}</div>', unsafe_allow_html=True)
        pdf_button("cl_view", f"CoverLetter_{job_target.replace(' ', '_')}.pdf")
