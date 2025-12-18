from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# --- Cargar modelo GPT-Neo 125M ---
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# --- Funciones GPT ---
def consultar_gpt(prompt, max_length=300):
    resultado = generator(prompt, max_length=max_length, num_return_sequences=1)
    return resultado[0]['generated_text']

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

