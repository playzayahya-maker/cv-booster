import streamlit as st
from groq import Groq

# 1. Basic Setup
st.set_page_config(page_title="CV Booster AI", page_icon="🚀", layout="wide")

# 2. Advanced CSS for Pro Look (Exactly like Screenshot 233)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    
    /* CV Paper Effect */
    .cv-paper {
        background-color: white;
        padding: 30px;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        font-family: 'Helvetica', sans-serif;
        color: #333;
        margin-bottom: 20px;
        border-top: 15px solid #3149A1; /* The Pro Blue Header Line */
    }
    
    .cv-section-title {
        color: #3149A1;
        border-bottom: 1px solid #EEE;
        padding-bottom: 5px;
        margin-top: 15px;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 14px;
    }
    
    .stButton>button { 
        background-color: #7C3AED; color: white; border-radius: 8px; font-weight: bold;
    }
    
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E5E7EB; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #7C3AED;'>📄 CV Booster</h2>", unsafe_allow_html=True)
    st.caption("Professional AI Optimizer")
    st.write("---")
    st.button("🏠 Home")
    st.button("🕒 History")
    st.info("AI Model: Llama 3.3 70B")

# 4. Input Section (Two Columns)
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.title("Build Your Pro Package")
    cv_input = st.text_area("Paste your current CV / Experience", height=300, placeholder="Ex: Ahmed, 3 years sales...")

with col_right:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("Target Details")
    job_title = st.text_input("Job Title", placeholder="e.g. Receptionist")
    region = st.selectbox("Region", ["Canada", "Europe", "USA"])
    
    # API KEY 
    MY_API_KEY = "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" # <--- -key 

    if st.button("Generate CV + Cover Letter ✨"):
        if cv_input and job_title and MY_API_KEY != "YOUR_GROQ_API_KEY_HERE":
            try:
                client = Groq(api_key=MY_API_KEY)
                with st.spinner("AI Agents are working..."):
                    
                    # AGENT 1: Professional CV (HTML Format)
                    cv_prompt = f"Rewrite this CV for {job_title} in {region}. Use clean HTML: <h3> for section titles, <ul> for bullets. Experience: {cv_input}"
                    cv_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": cv_prompt}])
                    st.session_state['final_cv'] = cv_res.choices[0].message.content
                    
                    # AGENT 2: Cover Letter (Text Format)
                    cl_prompt = f"Write a professional cover letter for {job_title} in {region} based on: {cv_input}. Formal tone."
                    cl_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": cl_prompt}])
                    st.session_state['final_cl'] = cl_res.choices[0].message.content
                    
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

# 5. Output Section (Separated Tabs)
if 'final_cv' in st.session_state:
    st.divider()
    st.subheader("Your Professional Results")
    
    # Tabs bach matkounch l-lettre de motivation mkhlta m3a l-CV
    tab_cv, tab_cl = st.tabs(["📄 Professional CV", "✉️ Cover Letter"])
    
    with tab_cv:
        # Display CV with the Blue/Purple Style
        st.markdown(f"<div class='cv-paper'>{st.session_state['final_cv']}</div>", unsafe_allow_html=True)
        st.download_button("Download CV (TXT)", st.session_state['final_cv'], file_name=f"CV_{job_title}.txt")
        
    with tab_cl:
        # Display Cover Letter separately
        st.markdown(f"<div class='cv-paper'>{st.session_state['final_cl']}</div>", unsafe_allow_html=True)
        st.download_button("Download Cover Letter (TXT)", st.session_state['final_cl'], file_name=f"Cover_Letter_{job_title}.txt")
