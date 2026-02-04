import streamlit as st
from groq import Groq

# 1. Setup
st.set_page_config(page_title="CV Booster AI", page_icon="🚀", layout="wide")

# 2. CSS Style (Screenshot 233 + 230 style)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .cv-paper {
        background-color: white;
        padding: 30px;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-top: 20px solid #3149A1; /* Pro Blue Header */
        margin-bottom: 20px;
    }
    .stButton>button { background-color: #7C3AED; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E5E7EB; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #7C3AED;'>📄 CV Booster</h2>", unsafe_allow_html=True)
    st.write("---")
    st.button("🏠 Home")
    st.button("🕒 History")

# 4. Main Layout (Two Columns)
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.title("Build Your Pro Package")
    
    # HNA ZDNA L-UPLOADER LI KAN KHASSAK
    uploaded_file = st.file_uploader("📤 Upload your old CV (PDF or DOCX)", type=["pdf", "docx"])
    
    st.markdown("--- or ---")
    cv_input = st.text_area("Paste CV text manually", height=250, placeholder="Ahmed, 3 years sales...")

with col_right:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("Target Details")
    job_title = st.text_input("Job Title", placeholder="e.g. Receptionist")
    region = st.selectbox("Region", ["Canada", "Europe", "USA"])
    
    # API KEY 
    MY_API_KEY = "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" # <--- L-KEY 

    if st.button("Generate CV + Cover Letter ✨"):
        if (cv_input or uploaded_file) and job_title and MY_API_KEY != "YOUR_GROQ_API_KEY_HERE":
            try:
                client = Groq(api_key=MY_API_KEY)
                with st.spinner("Processing..."):
                    # CV Agent
                    cv_res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"Create a professional CV for {job_title} in {region}. Use HTML: <h3> for titles, <ul> for bullets. Experience: {cv_input}"}]
                    )
                    st.session_state['final_cv'] = cv_res.choices[0].message.content
                    
                    # Cover Letter Agent
                    cl_res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"Write a professional cover letter for {job_title} in {region} based on this CV. Formal tone."}]
                    )
                    st.session_state['final_cl'] = cl_res.choices[0].message.content
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

# 5. Output with Separate Tabs
if 'final_cv' in st.session_state:
    st.divider()
    tab_cv, tab_cl = st.tabs(["📄 Optimized CV", "✉️ Professional Cover Letter"])
    
    with tab_cv:
        st.markdown(f"<div class='cv-paper'>{st.session_state['final_cv']}</div>", unsafe_allow_html=True)
        st.download_button("Download CV", st.session_state['final_cv'], file_name="pro_cv.txt")
        
    with tab_cl:
        st.markdown(f"<div class='cv-paper'>{st.session_state['final_cl']}</div>", unsafe_allow_html=True)
        st.download_button("Download Letter", st.session_state['final_cl'], file_name="cover_letter.txt")
