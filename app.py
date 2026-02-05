import streamlit as st
from groq import Groq
import streamlit.components.v1 as components
from PyPDF2 import PdfReader
import docx2txt

# 1. Page Config
st.set_page_config(page_title="Global CV Optimizer", page_icon="🌍", layout="wide")

# 2. Advanced CSS for Professional Display
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
    .stApp { background-color: #F8F9FA; }
    .doc-container {
        background-color: white;
        padding: 50px 60px;
        margin: auto;
        color: #000 !important;
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
        border: 1px solid #DDD;
        max-width: 800px;
    }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

# Helper function to extract text
def get_text_from_file(file):
    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            return "".join([page.extract_text() for page in reader.pages])
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return docx2txt.process(file)
    except Exception as e:
        return f"Error reading file: {e}"
    return None

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    MY_API_KEY = st.text_input("Groq API Key", type="password")
    region = st.selectbox("🌍 Select Target Region", ["Canada (Achievement-Based)", "Europe (Europass/Modern)"])
    st.divider()
    st.info("The AI will adjust the formatting and tone based on the selected region's recruitment standards.")

# 4. Main UI
st.title("ATS Multi-Region CV Optimizer")

col_in, col_settings = st.columns([1.5, 1], gap="large")

with col_in:
    st.subheader("📤 Upload or Paste CV")
    uploaded_file = st.file_uploader("Upload your current CV (PDF/DOCX)", type=["pdf", "docx"])
    cv_manual = st.text_area("Or paste content manually:", height=250)
    
    input_text = ""
    if uploaded_file:
        input_text = get_text_from_file(uploaded_file)
        st.success("✅ File loaded!")
    else:
        input_text = cv_manual

with col_settings:
    st.subheader("🎯 Job Details")
    job_title = st.text_input("Target Job Title", placeholder="e.g. Senior Marketing Manager")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        eng_lvl = st.select_slider("English", options=["Basic", "Intermediate", "Advanced", "Native"])
    with col_l2:
        fr_lvl = st.select_slider("French", options=["Basic", "Intermediate", "Advanced", "Native", "None"])
        
    generate_btn = st.button("✨ Optimize My CV Now")

# 5. AI Agent Logic
if generate_btn:
    if not MY_API_KEY:
        st.error("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")
    elif not input_text:
        st.warning("Please provide your CV content.")
    else:
        try:
            client = Groq(api_key=MY_API_KEY)
            with st.spinner(f"Restructuring for {region}..."):
                
                # Custom instructions based on region
                if "Canada" in region:
                    region_guidelines = (
                        "Use Canadian standards: Focus on quantitative ACHIEVEMENTS (metrics). "
                        "Reverse chronological order. Professional summary at the top integrating motivation. "
                        "NO personal details (age, photo). Plain, clean ATS-friendly layout."
                    )
                else:
                    region_guidelines = (
                        "Use European (Europass/Modern) standards: Structured sections, clear skills categorization. "
                        "Focus on both responsibilities and key projects. Professional and clean tone. "
                        "Include a 'Core Competencies' section clearly visible."
                    )

                prompt = f"""
                GUIDELINES: {region_guidelines}
                TARGET JOB: {job_title}
                LANGUAGES: English ({eng_lvl}), French ({fr_lvl})
                CV DATA: {input_text}
                
                Rewrite this CV to be 100% ATS-friendly. Use bold headers. No icons. No tables. 
                Ensure the final result looks professional when rendered in HTML.
                """

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are a world-class executive resume writer."},
                              {"role": "user", "content": prompt}]
                )
                st.session_state['cv_result'] = response.choices[0].message.content
        except Exception as e:
            st.error(f"Error: {e}")

# 6. Result & PDF Download
if 'cv_result' in st.session_state:
    st.divider()
    # Formatting for HTML
    final_html = st.session_state['cv_result'].replace("\n", "<br>").replace("**", "<b>")
    
    st.markdown(f'<div id="cv_output_final" class="doc-container">{final_html}</div>', unsafe_allow_html=True)
    
    if st.button("📥 Download My Optimized PDF"):
        # Improved JS for clean PDF export
        js_code = f"""
        <script>
            var element = window.parent.document.getElementById('cv_output_final');
            var opt = {{
                margin: [10, 15, 10, 15],
                filename: '{region.split(" ")[0]}_CV_{job_title.replace(" ", "_")}.pdf',
                image: {{ type: 'jpeg', quality: 0.98 }},
                html2canvas: {{ scale: 2, useCORS: true }},
                jsPDF: {{ unit: 'mm', format: 'a4', orientation: 'portrait' }}
            }};
            window.parent.html2pdf().from(element).set(opt).save();
        </script>
        """
        components.html(js_code, height=0)
