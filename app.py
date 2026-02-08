import streamlit as st
from groq import Groq
from fpdf import FPDF
import time

# --- 1. CONFIG & NEON DESIGN ---
st.set_page_config(page_title="ELITE CV ARCHITECT", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-header { color: #00FF9D; text-align: center; font-size: 40px; font-weight: 900; text-shadow: 0 0 20px #00FF9D44; }
    
    /* Neon Buttons Style */
    div.stButton > button {
        background-color: #0f172a; border: 2px solid #00FF9D; color: #00FF9D;
        width: 100%; height: 60px; font-size: 18px; font-weight: bold; border-radius: 12px;
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #00FF9D; color: #050505; box-shadow: 0 0 20px #00FF9D; }
    
    /* Region Style Selector */
    .stSelectbox label { color: #00FF9D !important; font-weight: bold; }
    
    /* Paper Preview */
    .paper-output { 
        background-color: white; color: #1a1a1a; padding: 40px; 
        border-radius: 5px; font-family: 'Garamond', serif; 
        box-shadow: 0 0 30px rgba(0,0,0,0.5); line-height: 1.6;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. PDF GENERATOR ---
def generate_pdf_bytes(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    # Clean text for Latin-1 (PDF Standard)
    safe_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, safe_text)
    return pdf.output()

# --- 3. SIDEBAR (API & INFO) ---
with st.sidebar:
    st.markdown("### 🔐 SECURITY")
    api_key = st.text_input("GROQ API KEY:", type="password")
    st.write("---")
    st.markdown("### 🛠 SYSTEM")
    st.caption("Engine: Llama-3.3-70B")
    st.caption("Status: Neural Parsing Active")

st.markdown("<h1 class='main-header'>NEURAL CV ARCHITECT PRO</h1>", unsafe_allow_html=True)

# --- 4. STYLE & INPUT SELECTION ---
col_style, col_mode = st.columns([1, 2])

with col_style:
    st.markdown("### 🌍 REGION STYLE")
    region = st.selectbox("Select Target Market:", ["CANADA (ATS Standard)", "USA (Corporate Style)", "EUROPE (Europass/Modern)"])

with col_mode:
    st.markdown("### 📥 INPUT SOURCE")
    input_choice = st.radio("Choose how to provide your data:", ["Paste Text (CV + Job)", "Upload File"], horizontal=True)

st.markdown("---")

# Data Holder
final_raw_data = ""

if input_choice == "Paste Text (CV + Job)":
    final_raw_data = st.text_area("Paste everything (Your Experience & The Job Offer) here:", height=350)
else:
    uploaded_file = st.file_uploader("Upload your old CV (PDF/JPG/PNG):", type=['pdf', 'png', 'jpg', 'jpeg', 'txt'])
    job_offer_text = st.text_area("Paste the Job Offer here:", height=200)
    if uploaded_file and job_offer_text:
        final_raw_data = f"USER CV: {uploaded_file.name}\nJOB OFFER: {job_offer_text}"

# --- 5. EXECUTION LOGIC ---
if st.button("EXECUTE ARCHITECT SCAN ⚡"):
    if not api_key:
        st.error("❌ Authentication Required: Enter API Key in the Sidebar.")
    elif not final_raw_data:
        st.warning("⚠️ Data Missing: Please provide your CV/Experience and the Job Offer.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.status("🧠 Processing Neural Architecture...", expanded=True) as status:
                st.write("📡 Detecting Job Title and ATS Keywords...")
                
                # Pro Prompt
                prompt = f"""
                You are a Master Executive Recruiter for the {region} market.
                
                INPUT DATA:
                {final_raw_data}
                
                YOUR TASK:
                1. Split the data into 'User Experience' and 'Job Requirements'.
                2. Create an Elite CV using STAR method.
                3. Create a High-Conversion Cover Letter for the {region} market.
                4. RULES: No photos/age if Canada/USA. Maximize keyword density.
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )
                
                st.session_state['result_text'] = completion.choices[0].message.content
                status.update(label="✅ ARCHITECTURE COMPLETE", state="complete")
                st.rerun() # Refresh bach i-ban l-output
        except Exception as e:
            st.error(f"Error: {e}")

# --- 6. RESULTS & EXPORT ---
if 'result_text' in st.session_state:
    st.markdown("### 📄 GENERATED ATS PACKAGE")
    st.markdown(f"<div class='paper-output'>{st.session_state['result_text']}</div>", unsafe_allow_html=True)
    
    # Generate PDF only when needed
    try:
        pdf_data = generate_pdf_bytes(st.session_state['result_text'])
        st.download_button(
            label="📥 DOWNLOAD PDF PACKAGE",
            data=pdf_data,
            file_name=f"Elite_CV_{region.split()[0]}.pdf",
            mime="application/pdf"
        )
    except Exception as pdf_err:
        st.error("PDF Engine Error. Please copy the text manually.")
