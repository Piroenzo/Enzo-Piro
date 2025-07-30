from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

# Ruta para obtener los proyectos
@app.route('/api/proyectos', methods=['GET'])
def get_proyectos():
    ruta = os.path.join(os.path.dirname(__file__), 'proyectos.json')
    with open(ruta, 'r') as archivo:
        proyectos = json.load(archivo)
    return jsonify(proyectos)

# Ruta para enviar correos
@app.route('/enviar', methods=['POST'])
def enviar_correo():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('email')
    mensaje = data.get('mensaje')

    msg = Message(f"Nuevo mensaje de {nombre}",
                  sender=correo,
                  recipients=[os.getenv("MAIL_USERNAME")])
    msg.body = mensaje
    mail.send(msg)
    return jsonify({"mensaje": "Correo enviado correctamente"})

if __name__ == '__main__':
    app.run(debug=True)
