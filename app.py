import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

# 1. Configuration dyal l-page
st.set_page_config(page_title="CV Booster Pro", page_icon="🚀", layout="wide")

# 2. CSS Style o JavaScript bach n-telechargiw PDF
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
    .stApp { background-color: #F8F9FA; }
    
    /* Container dial CV/Letter */
    .doc-container {
        background-color: white;
        padding: 40px;
        border-radius: 4px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-top: 20px solid #3149A1;
        margin-top: 20px;
        font-family: 'Arial', sans-serif;
        color: black !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #EEE; }
    
    /* Buttons */
    .stButton>button { 
        background-color: #7C3AED; color: white; border-radius: 8px; 
        font-weight: bold; width: 100%; height: 3.5em;
        border: none;
    }
    
    /* Formatting l-markdown wast l-container */
    .doc-container h1, .doc-container h2, .doc-container h3 { color: #3149A1; }
    .doc-container p, .doc-container li { color: #333; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation o API Key
with st.sidebar:
    st.markdown("<h2 style='color: #7C3AED;'>📄 CV Booster</h2>", unsafe_allow_html=True)
    st.caption("Professional AI Optimizer")
    st.write("---")
    
    # Blassa fin t-khchi l-API Key dialek
    MY_API_KEY = st.text_input("🔑 Groq API Key", type="password", placeholder="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")
    
    st.write("---")
    st.button("🏠 Inicio")
    st.button("🕒 Mis CVs")
    st.info("System: Llama 3.3 70B + PDF Export Support")

# 4. Input Section
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
        if not MY_API_KEY:
            st.error("Please enter your Groq API Key in the sidebar!")
        elif (cv_manual or uploaded_file) and job_target:
            try:
                client = Groq(api_key=MY_API_KEY)
                with st.spinner("AI is personalizing your documents..."):
                    input_data = cv_manual if cv_manual else "Document Content analysis"
                    
                    # 1. Optimized CV Agent
                    cv_query = f"Rewrite this CV for {job_target} in {region}. Use professional headers, bullet points, and clear sections. Context: {input_data}"
                    res_cv = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": cv_query}])
                    st.session_state['cv_final'] = res_cv.choices[0].message.content
                    
                    # 2. Cover Letter Agent (Moussa7a7 hna)
                    cl_query = f"Write a professional Cover Letter for {job_target} in {region}. Context: {input_data}"
                    res_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": cl_query}])
                    st.session_state['cl_final'] = res_cl.choices[0].message.content
                    
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

# 5. Output Section m3a PDF Download
if 'cv_final' in st.session_state:
    st.divider()
    tab_cv, tab_cl = st.tabs(["📄 Optimized CV", "✉️ Professional Cover Letter"])
    
    with tab_cv:
        # Id 'cv-content' bach n-qbdoh b JavaScript
        st.markdown(f'<div id="cv-content" class="doc-container">{st.session_state["cv_final"]}</div>', unsafe_allow_html=True)
        
        if st.button("📥 Download CV as PDF"):
            components.html(f"""
                <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
                <script>
                    const element = window.parent.document.getElementById('cv-content');
                    const opt = {{
                        margin: 0.5,
                        filename: 'CV_{job_target.replace(" ", "_")}.pdf',
                        image: {{ type: 'jpeg', quality: 0.98 }},
                        html2canvas: {{ scale: 2, useCORS: true }},
                        jsPDF: {{ unit: 'in', format: 'a4', orientation: 'portrait' }}
                    }};
                    html2pdf().set(opt).from(element).save();
                </script>
            """, height=0)

    with tab_cl:
        st.markdown(f'<div id="cl-content" class="doc-container">{st.session_state["cl_final"]}</div>', unsafe_allow_html=True)
        
        if st.button("📥 Download Letter as PDF"):
            components.html(f"""
                <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
                <script>
                    const element = window.parent.document.getElementById('cl-content');
                    const opt = {{
                        margin: 0.5,
                        filename: 'Letter_{job_target.replace(" ", "_")}.pdf',
                        image: {{ type: 'jpeg', quality: 0.98 }},
                        html2canvas: {{ scale: 2, useCORS: true }},
                        jsPDF: {{ unit: 'in', format: 'a4', orientation: 'portrait' }}
                    }};
                    html2pdf().set(opt).from(element).save();
                </script>
            """, height=0)
