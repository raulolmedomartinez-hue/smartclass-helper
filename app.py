import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import whisper
import tempfile
import os

# ------------------ CONFIG STREAMLIT ------------------
st.set_page_config(
    page_title="SmartClass Helper",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CARGA DE MODELOS (CACHE) ------------------
@st.cache_resource
def cargar_gpt():
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")
    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=-1
    )

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
    texto = st.text_area("Introduce el texto")
    if st.button("Resumir"):
        if not texto.strip():
            st.warning("⚠️ Introduce un texto")
        else:
            st.success(resumir_texto(texto))

elif opcion == "Ejercicios":
    texto = st.text_area("Introduce el tema")
    if st.button("Generar"):
        st.success(generar_ejercicios(texto))

elif opcion == "Organizador Tareas":
    texto = st.text_area("Introduce tus tareas")
    if st.button("Organizar"):
        st.success(organizar_tareas(texto))

elif opcion == "Explicador Ejercicios":
    texto = st.text_area("Introduce el ejercicio")
    if st.button("Explicar"):
        st.success(explicar_ejercicio(texto))

elif opcion == "Presentaciones":
    texto = st.text_area("Introduce el tema")
    if st.button("Generar"):
        st.success(generar_presentacion(texto))

elif opcion == "PDF → Resumen":
    archivo = st.file_uploader("Sube un PDF", type=["pdf"])
    if archivo:
        texto = leer_pdf(archivo)
        st.subheader("📄 Texto extraído")
        st.write(texto)
        st.subheader("📝 Resumen")
        st.success(resumir_texto(texto))

elif opcion == "Imagen → Texto":
    archivo = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])
    if archivo:
        texto = leer_imagen(archivo)
        st.subheader("🖼️ Texto detectado")
        st.write(texto)
        st.subheader("📝 Resumen")
        st.success(resumir_texto(texto))

elif opcion == "Audio → Transcripción":
    archivo = st.file_uploader("Sube audio", type=["mp3", "wav", "m4a"])
    if archivo:
        with st.spinner("Transcribiendo audio..."):
            texto = transcribir_audio(archivo)
        st.subheader("🎙️ Transcripción")
        st.write(texto)
        st.subheader("📝 Resumen")
        st.success(resumir_texto(texto))
