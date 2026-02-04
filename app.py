import streamlit as st
from groq import Groq
import time

# 1. Page Configuration
st.set_page_config(page_title="CV Booster AI", page_icon="📄", layout="wide")

# 2. Professional Purple Style (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #F9FAFB; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E5E7EB; }
    .stButton>button { 
        background-color: #7C3AED; color: white; border-radius: 8px; 
        border: none; padding: 12px; font-weight: 600; width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #6D28D9; box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3); }
    .stTextArea textarea { border-radius: 8px; border: 1px solid #D1D5DB; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Navigation in English)
with st.sidebar:
    st.markdown("<h2 style='color: #7C3AED;'>📄 CV Booster</h2>", unsafe_allow_html=True)
    st.caption("by Darcot")
    st.write("---")
    st.markdown("### NAVIGATION")
    st.button("🏠 Home")
    st.button("🕒 My CVs")
    st.button("🏢 Companies")
    st.write("---")
    st.info("✨ **Advanced AI**: Professional optimization with cutting-edge technology.")

# 4. Main Layout: Two Columns (Left for Input, Right for Options)
col_left, col_right = st.columns([1.5, 1], gap="large")

with col_left:
    st.title("Optimize Your CV")
    st.write("Transform your profile for International Markets (Canada, Europe, USA)")
    
    # Input Tabs
    tab1, tab2 = st.tabs(["📤 Upload File", "⌨️ Paste Text"])
    with tab1:
        st.file_uploader("Drop your CV here or click to select", type=["pdf", "docx"])
    with tab2:
        cv_content = st.text_area("Paste your CV content here", height=350, placeholder="Copy and paste your professional experience...")

with col_right:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("⚙️ Target Settings")
    
    # Target Job and Region
    job_title = st.text_input("Target Job Title", placeholder="e.g. Software Engineer")
    target_region = st.selectbox("Target Region", ["Canada", "European Union", "United States", "Middle East"])
    
    # Experience Level
    exp_level = st.selectbox("📊 Experience Level", ["Junior (0-2 years)", "Mid-Level (3-5 years)", "Senior (5+ years)"])
    
    # Sponsorship Checkbox
    sponsorship = st.checkbox("🤝 I need visa sponsorship")
    st.caption("We will prioritize companies that offer visa support.")

    # 📍 IMPORTANT: PUT YOUR GROQ API KEY HERE
    MY_API_KEY = "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" 

    if st.button("Generate Optimized CV →"):
        if cv_content and job_title and MY_API_KEY != "HNA_7ET_L_KEY_DYALK":
            try:
                client = Groq(api_key=MY_API_KEY)
                with st.status("Agents Running...", expanded=True) as status:
                    st.write("🔍 Analyzing structure...")
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"Optimize this CV for a {job_title} position in {target_region} for a {exp_level} level. Sponsorship needed: {sponsorship}. CV Content: {cv_content}"}]
                    )
                    st.session_state['result'] = response.choices[0].message.content
                    status.update(label="✅ Optimization Complete!", state="complete")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please provide your CV content and ensure the API Key is set.")

# 5. Result Section (Below the columns)
if 'result' in st.session_state:
    st.divider()
    st.subheader("✨ Your Optimized CV")
    st.markdown(st.session_state['result'])
    st.download_button("Download as Text", st.session_state['result'], file_name="optimized_cv.txt")
