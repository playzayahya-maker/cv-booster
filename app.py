import streamlit as st
from groq import Groq
import time

# 1. Config dyal l-page
st.set_page_config(page_title="CV Optimizer AI", page_icon="🚀", layout="wide")

# 2. Design Purple Style
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FC; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E6E8F1; }
    .stButton>button { 
        background-color: #6366F1; color: white; border-radius: 10px; 
        border: none; padding: 12px; font-weight: bold; width: 100%;
    }
    .stButton>button:hover { background-color: #4F46E5; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #6366F1;'>📄 CV Optimizer</h2>", unsafe_allow_html=True)
    st.write("v1.0 Agentic AI")
    st.write("---")
    st.info("Llama 3.3 Connected")

# 4. Main UI
st.title("CV Optimizer AI")
st.write("Transforma tu CV para el mercado internacional")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    cv_content = st.text_area("Pega tu CV aquí", height=300)
    job_target = st.text_input("Puesto objetivo (Ej: Developer in France)")
    
    # 📍 HNA DIR L-API KEY DYALK (OBLIGATOIRE)
    MY_API_KEY = "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" 

    if st.button("Generar CV Optimizado →"):
        if cv_content and job_target and MY_API_KEY != "HNA_7ET_L_KEY_DYALK":
            try:
                client = Groq(api_key=MY_API_KEY)
                with st.status("Procesando...", expanded=True) as status:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"Optimize this CV for {job_target}: {cv_content}"}]
                    )
                    st.session_state['result'] = response.choices[0].message.content
                    status.update(label="✅ ¡Completado!", state="complete")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Dakhal l-CV w l-API Key dyalk!")

with col2:
    st.subheader("Resultado")
    if 'result' in st.session_state:
        st.markdown(st.session_state['result'])
    else:
        st.info("El resultado aparecerá aquí.")
