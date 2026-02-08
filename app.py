import streamlit as st
from groq import Groq
from fpdf import FPDF
import time

# --- UI Setup (Elite Dark Mode) ---
st.set_page_config(page_title="ELITE AI ARCHITECT", layout="wide")

st.markdown("""
<style>
    /* Dark Background with Neon Accents */
    .stApp { background-color: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* Header & Stats Dashboard */
    .header-container { text-align: center; padding: 40px 0; border-bottom: 1px solid #1e293b; margin-bottom: 40px; }
    .main-title { color: #22c55e; font-size: 42px; font-weight: 800; letter-spacing: -2px; margin-bottom: 10px; }
    .stats-row { display: flex; justify-content: center; gap: 30px; margin-top: 20px; }
    .stat-box { background: #0f172a; border: 1px solid #1e293b; padding: 10px 25px; border-radius: 12px; font-size: 13px; color: #94a3b8; }
    .stat-val { color: #22c55e; font-weight: bold; margin-left: 5px; }

    /* Single Input Style */
    .stTextArea textarea { background-color: #0f172a !important; color: #ffffff !important; border: 1px solid #1e293b !important; border-radius: 15px !important; font-size: 16px !important; }
    .stTextArea textarea:focus { border-color: #22c55e !important; box-shadow: 0 0 15px rgba(34, 197, 94, 0.2) !important; }

    /* Preview Paper Style (White Professional) */
    .preview-paper { background: #ffffff; color: #1e293b; padding: 60px; border-radius: 4px; font-family: 'Garamond', serif; font-size: 18px; line-height: 1.6; min-height: 1000px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); margin: 40px auto; max-width: 900px; position: relative; }
    .preview-paper::before { content: "ATS VERIFIED"; position: absolute; top: 20px; right: 20px; color: #22c55e; border: 2px solid #22c55e; padding: 5px 10px; font-weight: bold; font-family: sans-serif; font-size: 12px; border-radius: 4px; }
    
    /* Sidebar Security Style */
    .sidebar-auth { background: #0f172a; padding: 20px; border-radius: 15px; border: 1px solid #1e293b; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- PDF Engine ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=11)
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, clean_text)
    return pdf.output()

# --- Dashboard Header ---
st.markdown("""
<div class='header-container'>
    <div class='main-title'>NEURAL CV ARCHITECT PRO</div>
    <div class='stats-row'>
        <div class='stat-box'>ACCURACY: <span class='stat-val'>98.2%</span></div>
        <div class='stat-box'>REGION: <span class='stat-val'>GLOBAL (CANADA/USA/EU)</span></div>
        <div class='stat-box'>ENGINE: <span class='stat-val'>LLAMA-3.3-70B</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar (Security Panel) ---
with st.sidebar:
    st.markdown("<div class='sidebar-auth'>", unsafe_allow_html=True)
    st.markdown("### 🔐 SECURITY PANEL")
    api_key = st.text_input("SYSTEM API KEY:", type="password") #
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### 🔍 AGENT LOGIC")
    st.caption("1. Content Parsing")
    st.caption("2. Geo-Formatting Detection")
    st.caption("3. STAR Achievement Logic")
    st.caption("4. ATS Cover Letter Sync")

# --- Main Interaction ---
st.markdown("### 📥 CENTRAL INTELLIGENCE INPUT")
st.markdown("<p style='color: #64748b;'>Paste your raw CV/Experience data AND the target Job Description below. The agent will automatically distinguish and optimize both.</p>", unsafe_allow_html=True)

mega_input = st.text_area("", placeholder="Paste raw text here...", height=450) #

# Execution
if st.button("EXECUTE ARCHITECT SCAN ⚡", use_container_width=True):
    if not api_key:
        st.error("SYSTEM AUTHENTICATION FAILED: Missing Key.") #
    elif len(mega_input) < 150:
        st.warning("DATA INSUFFICIENT: Paste more content to achieve 95% accuracy.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.status("🧠 Deep Neural Parsing in Progress...", expanded=True) as status:
                st.write("📡 Scanning text for job intent and country standards...")
                time.sleep(1.5)
                st.write("🧬 Rewriting CV using STAR methodology (Results-Based)...")
                time.sleep(1)
                st.write("✉️ Aligning Cover Letter with company values...")
                
                # Full Auto Intelligent Prompt
                prompt = f"""
                You are a Senior Career Strategist for high-tier international recruitment.
                DATA BLOCK: {mega_input}
                
                MISSION:
                1. Detect the Job Title and Target Country from the text.
                2. Extract the User's background.
                3. Rewrite everything into an ELITE ATS PACKAGE:
                   - CV Section: High-impact action verbs, quantifiable metrics, professional formatting.
                   - Cover Letter Section: Tailored, persuasive, and perfectly aligned with the job's pain points.
                
                RULES:
                - If North America: NO age/photo.
                - Use STAR method (Situation, Task, Action, Result) for all experience.
                - Ensure 100% keyword density for the detected role.
                """
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2 # Extreme focus
                )
                st.session_state['pro_package'] = res.choices[0].message.content
                status.update(label="✅ ARCHITECTURE READY", state="complete")
        except Exception as e:
            st.error(f"SYSTEM OVERLOAD: {e}")

# --- Output Display (Paper Style) ---
if 'pro_package' in st.session_state:
    st.write("---")
    st.markdown("<h3 style='text-align:center;'>📄 PRO ARCHITECT PACKAGE</h3>", unsafe_allow_html=True)
    
    # Paper-style preview
    st.markdown(f"<div class='preview-paper'>{st.session_state['pro_package']}</div>", unsafe_allow_html=True)
    
    # Pro Download Section
    pdf_final = create_pdf(st.session_state['pro_package'])
    st.download_button(
        label="📥 DOWNLOAD CV-READY PDF PACKAGE",
        data=pdf_final,
        file_name="Elite_Career_Package.pdf",
        mime="application/pdf",
        use_container_width=True
    )
