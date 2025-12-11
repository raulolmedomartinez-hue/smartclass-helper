import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import whisper
import os

# ---------------------------------------
# CONFIGURACIÓN API (SECRETS)
# ---------------------------------------
client = OpenAI(api_key=os.getenv("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"))

# ---------------------------------------
# FUNCIONES IA
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
# ESTILO Y TEMA
# ---------------------------------------
st.set_page_config(
    page_title="SmartClass Helper",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
/* General */
body, .stApp {
    background: linear-gradient(135deg, #a8edea, #fed6e3);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #0a1f44;
}

/* Encabezados */
h1, h2, h3 {
    color: #1f3b82;
    font-weight: bold;
}

/* Sidebar */
.css-1d391kg {  /* Cambia el color del sidebar */
    background-color: #1f3b82;
}
.css-1d391kg * {
    color: white;
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
.stTextArea textarea {
    border-radius: 12px;
    border: 2px solid #1f3b82;
    padding: 10px;
    background-color: #fff8f8;
}

/* Headers de sección */
.stSubheader {
    color: #ff4b5c;
    font-weight: bold;
}

/* Inputs de archivo */
.stFileUploader>div>div>input {
    border-radius: 10px;
}

/* Gradiente en títulos */
h1 {
    background: linear-gradient(90deg, #ff758c, #ff7eb3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
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
            st.success("✅ Resumen generado:")
            st.markdown(f"<div style='background:#fff0f5;padding:10px;border-radius:10px;'>{resumir_texto(texto)}</div>", unsafe_allow_html=True)

# ---------------------------- GENERADOR DE EJERCICIOS ----------------------------
elif opcion == "Ejercicios":
    st.subheader("📚 Generador de Ejercicios")
    texto = st.text_area("Introduce el tema")
    if st.button("Generar ejercicios"):
        if texto:
            st.success("✅ Ejercicios generados:")
            st.markdown(f"<div style='background:#f0fff0;padding:10px;border-radius:10px;'>{generar_ejercicios(texto)}</div>", unsafe_allow_html=True)

# ---------------------------- ORGANIZADOR DE TAREAS ----------------------------
elif opcion == "Organizador Tareas":
    st.subheader("📅 Organizador de Tareas")
    texto = st.text_area("Introduce tus tareas")
    if st.button("Organizar"):
        if texto:
            st.success("✅ Tareas organizadas:")
            st.markdown(f"<div style='background:#f0f8ff;padding:10px;border-radius:10px;'>{organizar_tareas(texto)}</div>", unsafe_allow_html=True)

# ---------------------------- EXPLICADOR DE EJERCICIOS ----------------------------
elif opcion == "Explicador Ejercicios":
    st.subheader("🧩 Explicador paso a paso")
    texto = st.text_area("Introduce el ejercicio")
    if st.button("Explicar"):
        if texto:
            st.success("✅ Explicación generada:")
            st.markdown(f"<div style='background:#fffaf0;padding:10px;border-radius:10px;'>{explicar_ejercicio(texto)}</div>", unsafe_allow_html=True)

# ---------------------------- GENERADOR DE PRESENTACIONES ----------------------------
elif opcion == "Presentaciones":
    st.subheader("🎤 Generador de Presentaciones")
    texto = st.text_area("Introduce el tema")
    if st.button("Generar Presentación"):
        if texto:
            st.success("✅ Presentación generada:")
            st.markdown(f"<div style='background:#f5fffa;padding:10px;border-radius:10px;'>{generar_presentacion(texto)}</div>", unsafe_allow_html=True)

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
        st.markdown(f"<div style='background:#fff0f5;padding:10px;border-radius:10px;'>{texto_transcrito}</div>", unsafe_allow_html=True)
        st.success("✅ Resumen del audio:")
        st.markdown(f"<div style='background:#f0fff0;padding:10px;border-radius:10px;'>{resumir_texto(texto_transcrito)}</div>", unsafe_allow_html=True)

