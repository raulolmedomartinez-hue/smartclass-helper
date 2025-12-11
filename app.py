import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import whisper

# ---------------------------------------
# CONFIGURACIÓN API
# ---------------------------------------
client = OpenAI(api_key="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")

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
/* Fondo y fuente general */
body {
    background-color: #f5f7fa;
    color: #0a1f44;
}

/* Encabezados */
h1, h2, h3 {
    color: #1f3b82;
}

/* Botones */
.stButton>button {
    background-color: #1f3b82;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

/* Área de texto */
.stTextArea textarea {
    border-radius: 10px;
    border: 2px solid #1f3b82;
    padding: 10px;
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
            st.success("Resumen generado:")
            st.write(resumir_texto(texto))

# ---------------------------- GENERADOR DE EJERCICIOS ----------------------------
elif opcion == "Ejercicios":
    st.subheader("📚 Generador de Ejercicios")
    texto = st.text_area("Introduce el tema")
    if st.button("Generar ejercicios"):
        if texto:
            st.success("Ejercicios generados:")
            st.write(generar_ejercicios(texto))

# ---------------------------- ORGANIZADOR DE TAREAS ----------------------------
elif opcion == "Organizador Tareas":
    st.subheader("📅 Organizador de Tareas")
    texto = st.text_area("Introduce tus tareas")
    if st.button("Organizar"):
        if texto:
            st.success("Tareas organizadas:")
            st.write(organizar_tareas(texto))

# ---------------------------- EXPLICADOR DE EJERCICIOS ----------------------------
elif opcion == "Explicador Ejercicios":
    st.subheader("🧩 Explicador paso a paso")
    texto = st.text_area("Introduce el ejercicio")
    if st.button("Explicar"):
        if texto:
            st.success("Explicación generada:")
            st.write(explicar_ejercicio(texto))

# ---------------------------- GENERADOR DE PRESENTACIONES ----------------------------
elif opcion == "Presentaciones":
    st.subheader("🎤 Generador de Presentaciones")
    texto = st.text_area("Introduce el tema")
    if st.button("Generar Presentación"):
        if texto:
            st.success("Presentación generada:")
            st.write(generar_presentacion(texto))

# ---------------------------- TRANSCRIPCIÓN DE AUDIO ----------------------------
elif opcion == "Transcripción Audio":
    st.subheader("🎙️ Transcripción y Resumen de Audio")
    archivo = st.file_uploader("Sube un archivo de audio (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])
    if archivo:
        modelo = whisper.load_model("base")
        resultado = modelo.transcribe(archivo.name)
        texto_transcrito = resultado["text"]
        st.success("Transcripción:")
        st.write(texto_transcrito)
        st.success("Resumen del audio:")
        st.write(resumir_texto(texto_transcrito))
