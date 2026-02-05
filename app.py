import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

# 1. Config dyal l-page
st.set_page_config(page_title="CV Booster Pro", page_icon="🚀", layout="wide")

# 2. CSS Style + JavaScript Logic
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
    /* Background o Font */
    .stApp { background-color: #F8F9FA; }
    
    /* Container dial CV o Letter */
    .doc-container {
        background-color: white;
        padding: 40px;
        border-radius: 4px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-top: 20px solid #3149A1;
        margin-top: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1a1a1a;
        line-height: 1.6;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #EEE; }
    
    /* Buttons style */
    .stButton>button { 
        background-color: #7C3AED; color: white; border-radius: 8px; 
        font-weight: bold; width: 100%; height: 3.5em;
        border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #6D28D9; border: none; }
    
    /* Headers inside the CV container */
    .doc-container h1, .doc-container h2 { color: #3149A1; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar: Fin idir l-API Key o Navigation
with st.sidebar:
    st.markdown("<h2 style='color: #7C3AED;'>📄 CV Booster</h2>", unsafe_allow_html=True)
    st.caption("Professional AI Optimizer")
    st.write("---")
    
    # --- INPUT API KEY ---
    api_key_input = st.sidebar.text_input("🔑 Groq API Key", type="password", help="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")
    
    st.write("---")
    st.button("🏠 Inicio")
    st.button("🕒 Mis CVs")
    st.info("System: Llama 3.3 70B + PDF Export Support")

# 4. Main Input Section
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.title("Build Your Pro Package")
    uploaded_file = st.file_uploader("📤 Upload CV (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg", "docx"])
    cv_manual = st.text_area("Or paste CV details here", height=250, placeholder="Copy-paste your experience...")

with col_right:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.subheader("Target Settings")
    job_target = st.text_input("Job Title", placeholder="e.g. Project Manager")
    region = st.selectbox("Target Region", ["Canada", "Europe", "USA", "Middle East"])
    
    if st.button("Generate Pro CV & Letter ✨"):
        if not api_key_input:
            st.warning("Please enter your API Key in the sidebar first!")
        elif (cv_manual or uploaded_file) and job_target:
            try:
                client = Groq(api_key=api_key_input)
                with st.spinner("AI is personalizing your documents..."):
                    input_text = cv_manual if cv_manual else "Analysis of uploaded document"
                    
                    # 1. Generate CV
                    cv_prompt = f"Rewrite this CV for a {job_target} position in {region}. Use professional HTML-friendly structure, clean headers, and bullet points. Content: {input_text}"
                    res_cv = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": cv_prompt}])
                    st.session_state['cv_final'] = res_cv.choices[0].message.content
                    
                    # 2. Generate Cover Letter
                    cl_prompt = f"Write a formal Cover Letter for {job_target}
