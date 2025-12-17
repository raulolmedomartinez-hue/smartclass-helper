import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import whisper
import tempfile
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="SmartClass Helper",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CARGA DE MODELOS ------------------
@st.cache_resource
def cargar_gpt():
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")
    return pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

@st.cache_resource
def cargar_whisper():
    return whisper.load_model("base")

generator = cargar_gpt()
modelo_whisper = cargar_whisper()

# ------------------ FUNCIONES IA ------------------
def consultar_gpt(prompt):
    resultado = generator(
        prompt,
        max_new_tokens=200,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.2
    )
    return resultado[0]["generated_text"]

def resumir_texto(texto):
    return consultar_gpt(f"Resume de forma clara y sencilla:\n{texto}")

def generar_ejercicios(texto):
    return consultar_gpt(f"Genera ejercicios con respuestas:\n{texto}")

def organizar_tareas(texto):
    return consultar_gpt(f"Organiza estas tareas por prioridad y fecha:\n{texto}")

def explicar_ejercicio(texto):
    return consultar_gpt(f"Explica paso a paso:\n{texto}")

def generar_presentacion(texto):
    return consultar_gpt(f"Crea una presentación con títulos y puntos clave:\n{texto}")

# ------------------ UTILIDADES ------------------
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

# ------------------ ENVIO DE CORREO CON SENDGRID ------------------
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

# ------------------ ESTILO ------------------
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(135deg, #a8edea, #fed6e3);
    font-family: 'Segoe UI';
}
h1 {
    background: linear-gradient(90deg, #ff758c, #ff7eb3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stButton>button {
    background: linear-gradient(45deg, #ff758c, #ff7eb3);
    color: white;
    border-radius: 15px;
    font-size: 16px;
    font-weight: bold;
}
.stTextArea textarea {
    background-color: white;
    color: black;
}
section[data-testid="stSidebar"] {
    background-color: #1f3b82;
}
section[data-testid="stSidebar"] * {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ------------------ INTERFAZ ------------------
st.title("🎓 SmartClass Helper")
st.markdown("Asistente inteligente para estudiar, organizar y aprender mejor.")

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

# ------------------ FUNCIONES ------------------
if opcion == "Resumidor":
    st.subheader("📝 Resumidor de Textos")
    texto = st.text_area("Introduce el texto")
    correo_destino = st.text_input("Introduce tu correo para recibir el resumen")
    if st.button("Resumir y enviar"):
        if not texto.strip():
            st.warning("Introduce un texto primero")
        elif not correo_destino.strip():
            st.warning("Introduce un correo válido")
        else:
            resumen = resumir_texto(texto)
            st.success("✅ Resumen generado:")
            st.markdown(f"<div style='background:#fff0f5;padding:10px;border-radius:10px;'>{resumen}</div>", unsafe_allow_html=True)
            
            # Enviar correo
            status = enviar_correo_sendgrid(correo_destino, "Resumen SmartClass", resumen)
            if status and status < 400:
                st.success(f"📧 Resumen enviado a {correo_destino} ✅")
            else:
                st.error("❌ No se pudo enviar el correo")

elif opcion == "Ejercicios":
    st.subheader("📚 Generador de Ejercicios")
    texto = st.text_area("Introduce el tema")
    correo_destino = st.text_input("Correo para recibir ejercicios")
    if st.button("Generar y enviar"):
        if not texto.strip():
            st.warning("Introduce un tema primero")
        elif not correo_destino.strip():
            st.warning("Introduce un correo válido")
        else:
            ejercicios = generar_ejercicios(texto)
            st.success("✅ Ejercicios generados:")
            st.markdown(f"<div style='background:#f0fff0;padding:10px;border-radius:10px;'>{ejercicios}</div>", unsafe_allow_html=True)
            status = enviar_correo_sendgrid(correo_destino, "Ejercicios SmartClass", ejercicios)
            if status and status < 400:
                st.success(f"📧 Ejercicios enviados a {correo_destino} ✅")
            else:
                st.error("❌ No se pudo enviar el correo")

elif opcion == "Organizador Tareas":
    st.subheader("📅 Organizador de Tareas")
    texto = st.text_area("Introduce tus tareas")
    correo_destino = st.text_input("Correo para recibir las tareas organizadas")
    if st.button("Organizar y enviar"):
        if not texto.strip():
            st.warning("Introduce las tareas primero")
        elif not correo_destino.strip():
            st.warning("Introduce un correo válido")
        else:
            tareas = organizar_tareas(texto)
            st.success("✅ Tareas organizadas:")
            st.markdown(f"<div style='background:#f0f8ff;padding:10px;border-radius:10px;'>{tareas}</div>", unsafe_allow_html=True)
            status = enviar_correo_sendgrid(correo_destino, "Tareas Organizadas SmartClass", tareas)
            if status and status < 400:
                st.success(f"📧 Tareas enviadas a {correo_destino} ✅")
            else:
                st.error("❌ No se pudo enviar el correo")

elif opcion == "Explicador Ejercicios":
    st.subheader("🧩 Explicador paso a paso")
    texto = st.text_area("Introduce el ejercicio")
    correo_destino = st.text_input("Correo para recibir la explicación")
    if st.button("Explicar y enviar"):
        if not texto.strip():
            st.warning("Introduce un ejercicio primero")
        elif not correo_destino.strip():
            st.warning("Introduce un correo válido")
        else:
            explicacion = explicar_ejercicio(texto)
            st.success("✅ Explicación generada:")
            st.markdown(f"<div style='background:#fffaf0;padding:10px;border-radius:10px;'>{explicacion}</div>", unsafe_allow_html=True)
            status = enviar_correo_sendgrid(correo_destino, "Explicación SmartClass", explicacion)
            if status and status < 400:
                st.success(f"📧 Explicación enviada a {correo_destino} ✅")
            else:
                st.error("❌ No se pudo enviar el correo")

elif opcion == "Presentaciones":
    st.subheader("🎤 Generador de Presentaciones")
    texto = st.text_area("Introduce el tema")
    correo_destino = st.text_input("Correo para recibir la presentación")
    if st.button("Generar y enviar"):
        if not texto.strip():
            st.warning("Introduce un tema primero")
        elif not correo_destino.strip():
            st.warning("Introduce un correo válido")
        else:
            presentacion = generar_presentacion(texto)
            st.success("✅ Presentación generada:")
            st.markdown(f"<div style='background:#f5fffa;padding:10px;border-radius:10px;'>{presentacion}</div>", unsafe_allow_html=True)
            status = enviar_correo_sendgrid(correo_destino, "Presentación SmartClass", presentacion)
            if status and status < 400:
                st.success(f"📧 Presentación enviada a {correo_destino} ✅")
            else:
                st.error("❌ No se pudo enviar el correo")

elif opcion == "PDF → Resumen":
    archivo = st.file_uploader("Sube un PDF", type=["pdf"])
    correo_destino = st.text_input("Correo para recibir el resumen")
    if archivo and st.button("Procesar y enviar"):
        texto = leer_pdf(archivo)
        st.subheader("📄 Texto extraído")
        st.write(texto)
        resumen = resumir_texto(texto)
        st.subheader("📝 Resumen")
        st.success(resumen)
        if correo_destino.strip():
            status = enviar_correo_sendgrid(correo_destino, "Resumen PDF SmartClass", resumen)
            if status and status < 400:
                st.success(f"📧 Resumen enviado a {correo_destino} ✅")
            else:
                st.error("❌ No se pudo enviar el correo")

elif opcion == "Imagen → Texto":
    archivo = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])
    correo_destino = st.text_input("Correo para recibir el resumen")
    if archivo and st.button("Procesar y enviar"):
        texto = leer_imagen(archivo)
        st.subheader("🖼️ Texto detectado")
        st.write(texto)
        resumen = resumir_texto(texto)
        st.subheader("📝 Resumen")
        st.success(resumen)
        if correo_destino.strip():
            status = enviar_correo_sendgrid(correo_destino, "Resumen Imagen SmartClass", resumen)
            if status and status < 400:
                st.success(f"📧 Resumen enviado a {correo_destino} ✅")
            else:
                st.error("❌ No se pudo enviar el correo")

elif opcion == "Audio → Transcripción":
    archivo = st.file_uploader("Sube audio", type=["mp3", "wav", "m4a"])
    correo_destino = st.text_input("Correo para recibir el resumen")
    if archivo and st.button("Transcribir y enviar"):
        with st.spinner("Transcribiendo audio..."):
            texto = transcribir_audio(archivo)
        st.subheader("🎙️ Transcripción")
        st.write(texto)
        resumen = resumir_texto(texto)
        st.subheader("📝 Resumen")
        st.success(resumen)
        if correo_destino.strip():
            status = enviar_correo_sendgrid(correo_destino, "Resumen Audio SmartClass", resumen)
            if status and status < 400:
                st.success(f"📧 Resumen enviado a {correo_destino} ✅")
            else:
                st.error("❌ No se pudo enviar el correo")
