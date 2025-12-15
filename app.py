import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import whisper
import os

# ---------------------------------------
# CLIENTE OPENAI (USANDO SECRETS)
# ---------------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------
# FUNCIONES DE IA
# ---------------------------------------
def consultar_gpt(prompt):
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente inteligente y amigable para estudiantes."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800
    )
    return respuesta.choices[0].message.content

def resumir_texto(texto):
    return consultar_gpt(f"Resume este texto de manera clara y sencilla:\n{texto}")

def generar_ejercicios(texto):
    return consultar_gpt(f"Genera ejercicios con respuestas sobre este texto:\n{texto}")

def organizar_tareas(texto):
    return consultar_gpt(f"Organiza estas tareas con prioridad y fecha:\n{texto}")

def explicar_ejercicio(texto):
    return consultar_gpt(f"Explica paso a paso este ejercicio:\n{texto}")

def generar_presentacion(texto):
    return consultar_gpt(f"Crea una presentación con títulos y puntos clave:\n{texto}")

# ---------------------------------------
# ESTILO Y TEMA MODERNO
# ---------------------------------------
st.set_page_config(
    page_title="SmartClass Helper",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Fondo general */
body, .stApp {
    background: linear-gradient(135deg, #a0c4ff, #bdb2ff);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #1a1a2e;
}

/* Sidebar */
.css-1d391kg {
    background-color: #4e4eff !important;
}
.css-1d391kg * {
    color: white !important;
}

/* Botones */
.stButton>button {
    background: linear-gradient(45deg, #ff758c, #ff7eb3);
    color: white;
    border-radius: 15px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Área de texto */
.stTextArea textarea, .stTextInput input {
    border-radius: 12px;
    border: 2px solid #4e4eff;
    padding: 10px;
    background-color: #f0f4f8;
    color: #1a1a2e;
}

/* Headers de sección */
h1, h2, h3 {
    font-weight: bold;
    background: linear-gradient(90deg, #ff758c, #ff7eb3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Gradientes en outputs */
.output-box {
    padding: 15px;
    border-radius: 12px;
    margin-top: 10px;
    background: linear-gradient(135deg, #caffbf, #9bf6ff);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# INTERFAZ STREAMLIT
# ---------------------------------------
st.title("🎓 SmartClass Helper")
st.markdown("Tu asistente inteligente para estudiar, organizar y aprender de manera eficiente.")

st.sidebar.title("Menú")
opcion = st.sidebar.selectbox("Selecciona la función", [
    "Resumidor",
    "Ejercicios",
    "Transcripción Audio",
    "Organizador Tareas",
    "Explicador Ejercicios",
    "Presentaciones"
])

# ---------------------------- RESUMIDOR ----------------------------
if opcion == "Resumidor":
    st.subheader("📝 Resumidor de Textos")
    texto = st.text_area("Introduce el texto")
    if st.button("Resumir"):
        if texto:
            resultado = resumir_texto(texto)
            st.success("✅ Resumen generado:")
            st.markdown(f"<div class='output-box'>{resultado}</div>", unsafe_allow_html=True)

# ---------------------------- GENERADOR DE EJERCICIOS ----------------------------
elif opcion == "Ejercicios":
    st.subheader("📚 Generador de Ejercicios")
    texto = st.text_area("Introduce el tema")
    if st.button("Generar ejercicios"):
        if texto:
            resultado = generar_ejercicios(texto)
            st.success("✅ Ejercicios generados:")
            st.markdown(f"<div class='output-box'>{resultado}</div>", unsafe_allow_html=True)

# ---------------------------- ORGANIZADOR DE TAREAS ----------------------------
elif opcion == "Organizador Tareas":
    st.subheader("📅 Organizador de Tareas")
    texto = st.text_area("Introduce tus tareas")
    if st.button("Organizar"):
        if texto:
            resultado = organizar_tareas(texto)
            st.success("✅ Tareas organizadas:")
            st.markdown(f"<div class='output-box'>{resultado}</div>", unsafe_allow_html=True)

# ---------------------------- EXPLICADOR DE EJERCICIOS ----------------------------
elif opcion == "Explicador Ejercicios":
    st.subheader("🧩 Explicador paso a paso")
    texto = st.text_area("Introduce el ejercicio")
    if st.button("Explicar"):
        if texto:
            resultado = explicar_ejercicio(texto)
            st.success("✅ Explicación generada:")
            st.markdown(f"<div class='output-box'>{resultado}</div>", unsafe_allow_html=True)

# ---------------------------- GENERADOR DE PRESENTACIONES ----------------------------
elif opcion == "Presentaciones":
    st.subheader("🎤 Generador de Presentaciones")
    texto = st.text_area("Introduce el tema")
    if st.button("Generar Presentación"):
        if texto:
            resultado = generar_presentacion(texto)
            st.success("✅ Presentación generada:")
            st.markdown(f"<div class='output-box'>{resultado}</div>", unsafe_allow_html=True)

# ---------------------------- TRANSCRIPCIÓN DE AUDIO ----------------------------
elif opcion == "Transcripción Audio":
    st.subheader("🎙️ Transcripción y Resumen de Audio")
    archivo = st.file_uploader("Sube un archivo de audio (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])
    if archivo:
        st.info("Procesando audio...")
        modelo = whisper.load_model("base")
        resultado = modelo.transcribe(archivo.name)
        texto_transcrito = resultado["text"]
        st.success("✅ Transcripción:")
        st.markdown(f"<div class='output-box'>{texto_transcrito}</div>", unsafe_allow_html=True)
        st.success("✅ Resumen del audio:")
        resumen = resumir_texto(texto_transcrito)
        st.markdown(f"<div class='output-box'>{resumen}</div>", unsafe_allow_html=True)

