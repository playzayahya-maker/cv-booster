import streamlit as st
from groq import Groq
import streamlit.components.v1 as components
from PyPDF2 import PdfReader
import docx2txt

# 1. Page Config
st.set_page_config(page_title="Global Career Package", page_icon="💼", layout="wide")

# 2. CSS Style (Clean & Executive)
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
    .stApp { background-color: #F8F9FA; }
    .doc-preview {
        background-color: white; padding: 50px 60px; margin: auto;
        color: #000 !important; font-family: 'Times New Roman', serif;
        line-height: 1.6; border: 1px solid #DDD; max-width: 800px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stButton>button { width: 100%; border-radius: 6px; font-weight: bold; background-color: #1A365D; color: white; height: 3.2em; }
    </style>
    """, unsafe_allow_html=True)

# Helper: Extract Text reliably
def extract_text(file):
    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
        return docx2txt.process(file)
    except Exception as e:
        return f"Error: {e}"

# 3. Sidebar
with st.sidebar:
    st.title("⚙️ Career Engine")
    api_key = st.text_input("🔑 Groq API Key", type="password")
    market = st.selectbox("🌍 Select Target Region", ["Canada (Achievement/STAR)", "Europe (Visa/Context/Skills)"])
    st.divider()
    st.success("ATS Algorithms: Integrated ✅")

# 4. Input Interface
st.title("Multi-Market CV & Cover Letter Pro")
c1, c2 = st.columns([1.2, 1], gap="large")

with c1:
    st.subheader("📤 Document Source")
    up_file = st.file_uploader("Upload Current CV (PDF/DOCX)", type=["pdf", "docx"])
    manual_text = st.text_area("Or Paste CV Content:", height=250)
    input_text = extract_text(up_file) if up_file else manual_text

with c2:
    st.subheader("🎯 Optimization Settings")
    job_target = st.text_input("Target Job Title", value="Digital Marketing Specialist")
    citizenship = st.text_input("Citizenship", placeholder="e.g. Moroccan")
    visa_status = st.text_input("Work Permit / Visa Status", placeholder="e.g. Sponsorship Needed")
    
    cl1, cl2 = st.columns(2)
    with cl1:
        eng = st.selectbox("English Level", ["Full Professional", "Bilingual", "Native"])
    with cl2:
        fr = st.selectbox("French Level", ["Professional Working", "Full Professional", "Native"])
    
    certs = st.text_input("Certifications", placeholder="Google, Meta Ads, HubSpot...")
    generate_btn = st.button("🚀 GENERATE FULL CAREER PACKAGE")

# 5. The AI Intelligence
if generate_btn:
    if not api_key:
        st.error("Please add your Groq API Key.")
    elif not input_text:
        st.warning("Please provide your CV content.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner(f"Engineering for {market} Market..."):
                is_europe = "Europe" in market
                
                rules = f"""
                - ATS RULES: Use bold headers, plain text, no tables, no icons.
                - HEADER: Include Citizenship: {citizenship} and Work Permit: {visa_status}.
                - SUMMARY: Results-driven, no emotional fluff. Mentions {job_target} and metrics.
                - EXPERIENCE: {'Add Industry Context (e.g. Tech Services, Retail) for each company.' if is_europe else 'Strictly use STAR method & Annualized metrics.'}
                - ACTION VERBS: Spearheaded, Orchestrated, Executed, Managed.
                - SKILLS: Add Adaptability, Intercultural Communication, Teamwork.
                - LANGUAGES: English ({eng}), French ({fr}).
                - CERTIFICATIONS: Create a dedicated section for {certs}.
                """

                # CV Generation
                cv_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Rewrite CV for {job_target} in {market}. Rules: {rules}. Data: {input_text}"}],
                    temperature=0.3
                )
                st.session_state['cv_final'] = cv_res.choices[0].message.content

                # Letter Generation
                cl_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Write a professional Cover Letter for {job_target} in {market} market based on: {input_text}."}],
                    temperature=0.4
                )
                st.session_state['cl_final'] = cl_res.choices[0].message.content
                st.balloons()
        except Exception as e:
            st.error(f"API Error: {e}")

# 6. Optimized Download Logic (Universal Fix)
def download_button(html_id, filename):
    components.html(f"""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
        <button onclick="dl()" style="width:100%; height:45px; background-color:#27ae60; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold; font-size:16px;">
            📥 Download {filename}
        </button>
        <script>
        function dl() {{
            const el = window.parent.document.getElementById('{html_id}');
            const opt = {{ margin: 15, filename: '{filename}', html2canvas: {{ scale: 2 }}, jsPDF: {{ format: 'a4' }} }};
            html2pdf().from(el).set(opt).save();
        }}
        </script>""", height=60)

# 7. Display Results
if 'cv_final' in st.session_state:
    st.divider()
    # Explicitly defining tabs to avoid NameError
    tab_cv, tab_cl = st.tabs(["📄 Optimized CV", "✉️ Professional Cover Letter"])
    
    with tab_cv:
        cv_clean = st.session_state['cv_final'].replace("\n", "<br>").replace("**", "<b>")
        st.markdown(f'<div id="cv_box" class="doc-preview">{cv_clean}</div>', unsafe_allow_html=True)
        download_button("cv_box", "Optimized_CV.pdf")
        
 # Create the tabs first
   t_cv, t_cl = st.tabs(["📄 Professional CV", "✉️ Cover Letter"])
  # Now you can use t_cl
     with t_cl:
    cl_clean = st.session_state['final_cl'].replace("\n", "<br>")
    st.markdown(f'<div id="cl_view" class="doc-preview">{cl_clean}</div>', unsafe_allow_html=True)
        
