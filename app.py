import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

# 1. Configuration
st.set_page_config(page_title="CV Booster Pro", page_icon="🚀", layout="wide")

# 2. CSS + JavaScript Fix (Added to the main body)
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
    .stApp { background-color: #F8F9FA; }
    .doc-container {
        background-color: white;
        padding: 50px;
        border-radius: 4px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        color: black !important;
        font-family: 'Times New Roman', serif; /* Standard for ATS */
        min-height: 800px;
    }
    .stButton>button { background-color: #7C3AED; color: white; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #7C3AED;'>📄 CV Booster</h2>", unsafe_allow_html=True)
    MY_API_KEY = st.text_input("🔑 Groq API Key", type="password")
    st.info("System: Llama 3.3 70B Optimized for ATS")

# 4. Input Section
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.title("Build Your Pro Package")
    cv_manual = st.text_area("Paste your current CV here", height=300)

with col_right:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    job_target = st.text_input("Target Job Title", placeholder="e.g. Digital Marketing Specialist")
    region = st.selectbox("Target Region", ["Canada", "Europe", "USA", "Middle East"])
    
    generate_btn = st.button("Generate Pro CV & Letter ✨")

# 5. Logic & AI Agents
if generate_btn:
    if not MY_API_KEY:
        st.error("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")
    elif not cv_manual or not job_target:
        st.warning("Please fill in your CV data and Job Title.")
    else:
        try:
            client = Groq(api_key=MY_API_KEY)
            with st.spinner("AI is crafting ATS-optimized documents..."):
                # System Prompt for ATS optimization
                sys_prompt = "You are an expert ATS (Applicant Tracking System) optimizer. " \
                             "Use professional headings, no columns, no tables, and use industry keywords."

                # CV Prompt
                cv_query = f"Rewrite this CV for a {job_target} position in {region}. Focus on measurable achievements (metrics) and include a 'Core Competencies' section. CV Data: {cv_manual}"
                res_cv = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": cv_query}]
                )
                st.session_state['cv_final'] = res_cv.choices[0].message.content

                # Cover Letter Prompt
                cl_query = f"Write a professional cover letter for {job_target} in {region}. Context: {cv_manual}"
                res_cl = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": cl_query}]
                )
                st.session_state['cl_final'] = res_cl.choices[0].message.content
                st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")

# 6. Display & Download
if 'cv_final' in st.session_state:
    tab_cv, tab_cl = st.tabs(["📄 Optimized CV", "✉️ Cover Letter"])
    
    with tab_cv:
        # We wrap the content in a div with a specific ID for the JS to find
        cv_html = f'<div id="cv_download_area" class="doc-container">{st.session_state["cv_final"].replace("\n", "<br>")}</div>'
        st.markdown(cv_html, unsafe_allow_html=True)
        
        if st.button("📥 Download CV as PDF"):
            js_code = f"""
                <script>
                    var element = window.parent.document.getElementById('cv_download_area');
                    var opt = {{
                        margin: 10,
                        filename: 'CV_{job_target.replace(" ", "_")}.pdf',
                        image: {{ type: 'jpeg', quality: 0.98 }},
                        html2canvas: {{ scale: 2 }},
                        jsPDF: {{ unit: 'mm', format: 'a4', orientation: 'portrait' }}
                    }};
                    window.parent.html2pdf().from(element).set(opt).save();
                </script>
            """
            components.html(js_code, height=0)

    with tab_cl:
        cl_html = f'<div id="cl_download_area" class="doc-container">{st.session_state["cl_final"].replace("\n", "<br>")}</div>'
        st.markdown(cl_html, unsafe_allow_html=True)
        
        if st.button("📥 Download Letter as PDF"):
            js_code = f"""
                <script>
                    var element = window.parent.document.getElementById('cl_download_area');
                    var opt = {{
                        margin: 10,
                        filename: 'Letter_{job_target.replace(" ", "_")}.pdf',
                        image: {{ type: 'jpeg', quality: 0.98 }},
                        html2canvas: {{ scale: 2 }},
                        jsPDF: {{ unit: 'mm', format: 'a4', orientation: 'portrait' }}
                    }};
                    window.parent.html2pdf().from(element).set(opt).save();
                </script>
            """
            components.html(js_code, height=0)
