import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="Canada CV ATS Pro", page_icon="🇨🇦", layout="wide")

# 2. Advanced CSS & JS for PDF Generation
st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
    .stApp { background-color: #F4F7F9; }
    
    /* Document Style: Clean, Professional, No Graphics for ATS */
    .doc-container {
        background-color: white;
        padding: 45px 60px;
        margin: auto;
        color: #000 !important;
        font-family: 'Times New Roman', serif; /* Best for ATS */
        line-height: 1.5;
        border: 1px solid #EEE;
    }
    
    .stButton>button {
        background-color: #C53030;
        color: white;
        font-weight: bold;
        border-radius: 4px;
        border: none;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #C53030;'>🇨🇦 Canada Resume Builder</h2>", unsafe_allow_html=True)
    st.write("---")
    MY_API_KEY = st.text_input("🔑 Groq API Key", type="password", help="Enter your gsk_... key here")
    st.info("💡 **Tip:** In Canada, don't include your photo, age, or marital status to avoid bias.")

# 4. Inputs
st.title("Professional CV Optimizer")
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Current CV Details")
    cv_text = st.text_area("Paste your current CV / Experience:", height=300, 
                           placeholder="Yassine El Amrani - Digital Marketing Specialist...")
    
    certifications = st.text_input("Certifications (Optional)", placeholder="e.g. Google Ads, HubSpot, Blueprint")

with col2:
    st.subheader("Target & Languages")
    job_target = st.text_input("Job Title You're Applying For", value="Digital Marketing Specialist")
    
    lang_col1, lang_col2 = st.columns(2)
    with lang_col1:
        eng_lvl = st.selectbox("English Proficiency", ["Bilingual", "Professional Working", "Full Professional", "Native"])
    with lang_col2:
        fr_lvl = st.selectbox("French Proficiency", ["Professional Working", "Bilingual", "Native", "Basic", "None"])

    generate_btn = st.button("Generate & Optimize for Canada ✨")

# 5. AI Logic
if generate_btn:
    if not MY_API_KEY:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not cv_text:
        st.warning("Please paste your CV content.")
    else:
        try:
            client = Groq(api_key=MY_API_KEY)
            with st.spinner("AI is restructuring your CV for Canadian ATS standards..."):
                
                # System Prompt: Strict Canadian ATS Rules
                sys_msg = (
                    "You are a Senior Canadian Recruiter. Rewrite the user's CV to pass ATS filters. "
                    "1. Combine the professional summary with their motivation at the top. "
                    "2. Transform responsibilities into quantitative ACHIEVEMENTS (use numbers/metrics). "
                    "3. Use standard headers: PROFESSIONAL SUMMARY, CORE COMPETENCIES, PROFESSIONAL EXPERIENCE, EDUCATION, CERTIFICATIONS, and LANGUAGES. "
                    "4. Remove any mention of 'Open to relocation' - keep only the current city. "
                    "5. Use action verbs (Spearheaded, Optimized, Orchestrated). "
                    "Format the output in clean Markdown with bold headers."
                )
                
                user_msg = f"""
                Target Job: {job_target}
                Languages: English ({eng_lvl}), French ({fr_lvl})
                Certifications: {certifications}
                CV Data: {cv_text}
                """

                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": sys_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=0.3 # Low temperature for professional accuracy
                )
                
                st.session_state['final_cv'] = chat_completion.choices[0].message.content
                st.balloons()

        except Exception as e:
            st.error(f"Error: {e}")

# 6. Display & Download
if 'final_cv' in st.session_state:
    st.write("---")
    st.subheader("Preview Your Optimized CV")
    
    # Convert Markdown to HTML for the PDF generator
    cv_markdown = st.session_state['final_cv']
    # Small trick to handle markdown lines for HTML rendering
    cv_html_ready = cv_markdown.replace("\n", "<br>").replace("### ", "<h3>").replace("## ", "<h2>").replace("**", "<b>").replace("<b> ", "<b>")

    # The Container for PDF
    st.markdown(f'<div id="printable_cv" class="doc-container">{cv_html_ready}</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("📥 Download PDF"):
        # JavaScript for high-quality PDF export
        js_download = f"""
        <script>
            var element = window.parent.document.getElementById('printable_cv');
            var opt = {{
                margin: [15, 15, 15, 15],
                filename: 'CV_Canada_{job_target.replace(" ", "_")}.pdf',
                image: {{ type: 'jpeg', quality: 0.98 }},
                html2canvas: {{ scale: 3, useCORS: true, letterRendering: true }},
                jsPDF: {{ unit: 'mm', format: 'a4', orientation: 'portrait' }}
            }};
            window.parent.html2pdf().from(element).set(opt).save();
        </script>
        """
        components.html(js_download, height=0)
