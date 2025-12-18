import streamlit as st
from gpt_utils import resumir_texto, generar_ejercicios, organizar_tareas, explicar_ejercicio, generar_presentacion
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import whisper
import tempfile
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

st.set_page_config(page_title="SmartClass Helper", page_icon="🎓", layout="wide")

# --- Carga de modelos ---
@st.cache_resource
def cargar_whisper():
    return whisper.load_model("base")

modelo_whisper = cargar_whisper()

# --- Funciones auxiliares ---
def leer_pdf(archivo):
    reader = PdfReader(archivo)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text()
    return texto

def leer_imagen(archivo):
    imagen = Image.open(archivo)
    return pytesseract.image_to_string(imagen)

def transcribir_audio(archivo):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(archivo.read())
        ruta = tmp.name
    resultado = modelo_whisper.transcribe(ruta)
    os.remove(ruta)
    return resultado["text"]

def enviar_correo_sendgrid(destinatario, asunto, mensaje):
    mail = Mail(
        from_email='raulolmedomartinez@gesanmiguel2.com',
        to_emails=destinatario,
        subject=asunto,
        plain_text_content=mensaje
    )
    try:
        sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
        response = sg.send(mail)
        return response.status_code
    except Exception as e:
        st.error(f"Error al enviar correo: {e}")
        return None

# --- Interfaz ---
st.title("🎓 SmartClass Helper")
st.sidebar.title("📚 Menú")
opcion = st.sidebar.selectbox("Selecciona una función", [
    "Resumidor",
    "Ejercicios",
    "Organizador Tareas",
    "Explicador Ejercicios",
    "Presentaciones",
    "PDF → Resumen",
    "Imagen → Texto",
    "Audio → Transcripción"
])

# --- Funciones Streamlit ---
def procesar_texto(funcion, texto, correo_destino, asunto):
    resultado = funcion(texto)
    st.success(resultado)
    if correo_destino.strip():
        status = enviar_correo_sendgrid(correo_destino, asunto, resultado)
        if status and status < 400:
            st.success(f"📧 Enviado a {correo_destino} ✅")
        else:
            st.error("❌ No se pudo enviar el correo")
    return resultado

# --- Opciones ---
if opcion == "Resumidor":
    texto = st.text_area("Introduce el texto")
    correo = st.text_input("Correo")
    if st.button("Resumir y enviar"):
        if texto.strip() and correo.strip():
            procesar_texto(resumir_texto, texto, correo, "Resumen SmartClass")

elif opcion == "Ejercicios":
    texto = st.text_area("Introduce el tema")
    correo = st.text_input("Correo")
    if st.button("Generar y enviar"):
        if texto.strip() and correo.strip():
            procesar_texto(generar_ejercicios, texto, correo, "Ejercicios SmartClass")

elif opcion == "Organizador Tareas":
    texto = st.text_area("Introduce tus tareas")
    correo = st.text_input("Correo")
    if st.button("Organizar y enviar"):
        if texto.strip() and correo.strip():
            procesar_texto(organizar_tareas, texto, correo, "Tareas Organizadas SmartClass")

elif opcion == "Explicador Ejercicios":
    texto = st.text_area("Introduce el ejercicio")
    correo = st.text_input("Correo")
    if st.button("Explicar y enviar"):
        if texto.strip() and correo.strip():
            procesar_texto(explicar_ejercicio, texto, correo, "Explicación SmartClass")

elif opcion == "Presentaciones":
    texto = st.text_area("Introduce el tema")
    correo = st.text_input("Correo")
    if st.button("Generar y enviar"):
        if texto.strip() and correo.strip():
            procesar_texto(generar_presentacion, texto, correo, "Presentación SmartClass")

elif opcion == "PDF → Resumen":
    archivo = st.file_uploader("Sube un PDF", type=["pdf"])
    correo = st.text_input("Correo")
    if archivo and st.button("Procesar y enviar"):
        texto = leer_pdf(archivo)
        procesar_texto(resumir_texto, texto, correo, "Resumen PDF SmartClass")

elif opcion == "Imagen → Texto":
    archivo = st.file_uploader("Sube imagen", type=["png","jpg","jpeg"])
    correo = st.text_input("Correo")
    if archivo and st.button("Procesar y enviar"):
        texto = leer_imagen(archivo)
        procesar_texto(resumir_texto, texto, correo, "Resumen Imagen SmartClass")

elif opcion == "Audio → Transcripción":
    archivo = st.file_uploader("Sube audio", type=["mp3","wav","m4a"])
    correo = st.text_input("Correo")
    if archivo and st.button("Transcribir y enviar"):
        texto = transcribir_audio(archivo)
        procesar_texto(resumir_texto, texto, correo, "Resumen Audio SmartClass")
