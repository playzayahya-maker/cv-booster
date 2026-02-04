import streamlit as st
from groq import Groq
import time

# 1. Config dyal l-page (Smiya w l-icon)
st.set_page_config(page_title="CV Optimizer AI", page_icon="🚀", layout="wide")

# 2. Design (CSS) - Purple Style dyal Startgate
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FC; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E6E8F1; }
    .stButton>button { 
        background-color: #6366F1; color: white; border-radius: 10px; 
        border: none; padding: 12px; font-weight: bold; width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #4F46E5; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); }
    .stTextArea textarea { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Navigation)
with st.sidebar:
    st.markdown("<h2 style='color: #6366F1;'>📄 CV Optimizer</h2>", unsafe_allow_html=True)
    st.write("Agentic AI System v1.0")
    st.write("---")
    st.button("🏠 Inicio")
    st.button("🕒 Mis CVs")
    st.button("🏢 Empresas")
    st.markdown("---")
    st.success("**Status**: Online")
    st.info("Powered by Llama 3.3 70B")

# 4. Main Interface
st.title("CV Optimizer AI")
st.write("Transforma tu perfil profesional para el mercado internacional (Canadá, Europa, etc.)")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📥 Datos de Entrada")
    tab1, tab2 = st.tabs(["📤 Subir PDF", "⌨️ Pegar Texto"])
    
    with tab2:
        cv_content = st.text_area("Pega el contenido de tu CV aquí", height=250, placeholder="Copia y pega tu experiencia profesional...")
    
    with tab1:
        st.file_uploader("Seleccionar Archivo PDF", type=["pdf"])
        st.caption("Nota: La función de subida directa estará disponible pronto.")

    job_target = st.text_input("Puesto objetivo y País", placeholder="Ej: Receptionist in Canada")
    
    # ---------------------------------------------------------
    # 📍 HNA T-7ET L-API KEY DYALK (OBLIGATOIRE)
    # ---------------------------------------------------------
    MY_API_KEY = "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" 
    # ---------------------------------------------------------

    if st.button("Generar CV Optimizado →"):
        if cv_content and job_target and MY_API_KEY != "HNA_7ET_L_KEY_DYALK":
            try:
                client = Groq(api_key=MY_API_KEY)
                
                with st.status("Ejecutando Agentes de IA...", expanded=True) as status:
                    st.write("🔍 **Agent 1**: Analizando estructura del CV...")
                    time.sleep(1)
                    st.write("🤖 **Agent 2**: Optimizando palabras clave (ATS)...")
                    
                    # AI Call
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"Optimize this CV for {job_target} focusing on Canada/Europe standards: {cv_content}"}],
                        temperature=0.3
                    )
