from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from gpt_utils import organizar_tareas
import os

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    mensaje = request.form.get("Body", "")
    if not mensaje.strip():
        mensaje = "No se recibió texto"

    respuesta = organizar_tareas(mensaje)
    resp = MessagingResponse()
    resp.message("📅 *Tareas organizadas*\n\n" + respuesta)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

