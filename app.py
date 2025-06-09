import os
import json
from flask import Flask, request, jsonify
from firebase_admin import credentials, initialize_app, db

app = Flask(__name__)

# 🔐 Leer el contenido del JSON desde una variable de entorno
firebase_json = os.getenv("FIREBASE_CONFIG")

if not firebase_json:
    raise ValueError("La variable de entorno FIREBASE_CONFIG no está definida.")

cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)

initialize_app(cred, {
    "databaseURL": "https://usuarios-5be49-default-rtdb.firebaseio.com/"
})

@app.route("/")
def index():
    return "✅ Microservicio de registro operativo."

@app.route("/registrar", methods=["POST"])
def registrar():
    data = request.get_json()
    numero = data.get("numero")
    nombre = data.get("nombre")

    if not numero or not nombre:
        return jsonify({"error": "Faltan datos"}), 400

    ref = db.reference("/usuarios")
    ref.child(numero).set(nombre)

    return jsonify({"registrado": True, "nombre": nombre})

# 🔁 Bloque necesario para que Render detecte el puerto
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
