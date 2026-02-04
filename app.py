import streamlit as st
from groq import Groq

# 1. Config dyal l-page
st.set_page_config(page_title="CV Booster Pro", page_icon="🚀", layout="wide")

# 2. CSS Style (The "Screenshot 233" Professional Look)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    
    /* CV/Letter Container */
    .doc-container {
        background-color: white;
        padding: 40px;
        border-radius: 4px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-top: 20px solid #3149A1; /* Pro Blue Header */
        margin-top: 20px;
        font-family: 'Arial', sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #EEE; }
    
    /* Buttons */
    .stButton>button { 
        background-color: #7C3AED; color: white; border-radius: 8px; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='color: #7C3AED;'>📄 CV Booster</h2>", unsafe_allow_html=True)
    st.caption("Professional AI Optimizer")
    st.write("---")
    st.button("🏠 Inicio")
    st.button("🕒 Mis CVs")
    st.info("System: Llama 3.3 70B + OCR Support")

# 4. Input Section (2 Columns)
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.title("Build Your Pro Package")
    # Supports Images and PDFs
    uploaded_file = st.file_uploader("📤 Upload CV (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg", "docx"])
    cv_manual = st.text_area("Or paste CV details here", height=250, placeholder="Copy-paste your experience...")

with col_right:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.subheader("Target Settings")
    job_target = st.text_input("Job Title", placeholder="e.g. Project Manager")
    region = st.selectbox("Target Region", ["Canada", "Europe", "USA", "Middle East"])
    
    # 📍 API KEY (Badel hadi b dyalk!)
    MY_API_KEY = "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" 

    if st.button("Generate Pro CV & Letter ✨"):
        if (cv_manual or uploaded_file) and job_target and MY_API_KEY != "HNA_7ET_L_KEY_DYALK":
            try:
                client = Groq(api_key=MY_API_KEY)
                with st.spinner("AI is personalizing your documents..."):
                    # Process Input
                    input_data = cv_manual if cv_manual else "Document Content"
                    
                    # 1. Optimized CV Agent (Markdown)
                    cv_query = f"Rewrite this CV for {job_target} in {region}. Use professional headers, bullet points, and clear sections. Context: {input_data}"
                    res_cv = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": cv_query}])
                    st.session_state['cv_final'] = res_cv.choices[0].message.content
                    
                    # 2. Personalized Cover Letter Agent
                    cl_query = f"Write a professional Cover Letter for {job_target} in {region}. Extract the user's name from the CV and use it as the signature. Context: {input_data}"
                    res_cl = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": cl_query}])
                    st.session_state['cl_final'] = res_cl.choices[0].message.content
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

# 5. Output Section (Separated Tabs)
if 'cv_final' in st.session_state:
    st.divider()
    st.subheader("✨ Your Professional Results")
    
    # Separation d l-CV 3la l-Letter
    tab_cv, tab_cl = st.tabs(["📄 Optimized CV", "✉️ Professional Cover Letter"])
    
    with tab_cv:
        st.markdown('<div class="doc-container">', unsafe_allow_html=True)
        st.markdown(st.session_state['cv_final'])
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button("Download CV", st.session_state['cv_final'], file_name=f"CV_{job_target}.txt")
        
    with tab_cl:
        st.markdown('<div class="doc-container">', unsafe_allow_html=True)
        st.markdown(st.session_state['cl_final'])
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button("Download Letter", st.session_state['cl_final'], file_name=f"Letter_{job_target}.txt")
