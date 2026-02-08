import streamlit as st
from groq import Groq
from fpdf import FPDF
import time

# --- UI Setup ---
st.set_page_config(page_title="NEURAL ARCHITECT PRO", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .main-header { color: #22c55e; text-align: center; font-size: 35px; font-weight: 800; padding: 20px; }
    
    /* Style d les Buttons d Toggle */
    .toggle-container { display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; }
    .stButton>button { width: 200px; border-radius: 10px; font-weight: bold; transition: 0.3s; }
    
    /* Paper Style Preview */
    .preview-paper { background: white; color: #1e293b; padding: 50px; border-radius: 5px; font-family: 'Garamond', serif; min-height: 800px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); line-height: 1.6; margin-top: 30px; }
</style>
""", unsafe_allow_html=True)

# --- PDF Engine ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=12)
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    return pdf.output()

# --- Sidebar API ---
with st.sidebar:
    st.markdown("### 🔐 SYSTEM ACCESS")
    api_key = st.text_input("GROQ API KEY:", type="password")
    st.write("---")
    st.info("Mode: Smart Toggle\nAuto-Parsing: Active")

st.markdown("<div class='main-header'>NEURAL CV ARCHITECT PRO</div>", unsafe_allow_html=True)

# --- Smart Toggle Logic ---
if 'input_mode' not in st.session_state:
    st.session_state.input_mode = None

st.markdown("<h4 style='text-align:center;'>Khtar kifach bghiti t-7et profile dyalk:</h4>", unsafe_allow_html=True)
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("📁 UPLOAD CV (IMAGE/PDF)"):
        st.session_state.input_mode = 'file'

with col_btn2:
    if st.button("⌨️ PASTE RAW TEXT"):
        st.session_state.input_mode = 'text'

# --- Hidden Input Areas ---
user_data = ""

if st.session_state.input_mode == 'file':
    st.markdown("---")
    # Hna t9der t-uploadi Image wlla PDF
    uploaded_file = st.file_uploader("Uploadi l-CV l-9dim (Image/PDF/TXT):", type=['pdf', 'txt', 'png', 'jpg', 'jpeg'])
    if uploaded_file:
        # Ila image, khass OCR (hadi faza khera), walakin t9der t-readiha ka bytes
        user_data = f"File Uploaded: {uploaded_file.name}"
        st.success(f"✅ {uploaded_file.name} Ready for Scan")

elif st.session_state.input_mode == 'text':
    st.markdown("---")
    user_data = st.text_area("Paste CV Text + Job Description hna:", height=300, placeholder="Copy kolshi hna...")

# --- Common Job Description Area (ila knti baghi t-khlliha dima bayna) ---
# (Optionnel: L-Agent t-i-parsingi kolchi mn kadr wa7ed kif glti)

# --- Execution ---
if st.button("EXECUTE PRO SCAN ⚡", use_container_width=True):
    if not api_key:
        st.error("Missing API Key in Sidebar!")
    elif not user_data:
        st.warning("Please provide your data first.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.status("🧠 Processing Data...", expanded=True) as status:
                st.write("📡 Separating profile from job requirements...")
                
                # Intelligent Prompt for parsing
                prompt = f"""
                You are an Elite Recruiter. Analyze the provided input. 
                Identify the Job Title and Location. 
                Create an ATS-Optimized CV (STAR Method) and a professional Cover Letter.
                
                INPUT DATA:
                {user_data}
                
                Formatting: Canada/USA professional standards.
                """
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )
                st.session_state['final_out'] = res.choices[0].message.content
                status.update(label="✅ ARCHITECTURE COMPLETE", state="complete")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Result Display ---
if 'final_out' in st.session_state:
    st.markdown("<div class='preview-paper'>" + st.session_state['final_out'] + "</div>", unsafe_allow_html=True)
    
    pdf_bytes = create_pdf(st.session_state['final_out'])
    st.download_button(
        label="📥 DOWNLOAD PDF PACKAGE",
        data=pdf_bytes,
        file_name="Elite_Package.pdf",
        mime="application/pdf",
        use_container_width=True
    )
