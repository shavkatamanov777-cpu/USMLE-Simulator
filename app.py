import os
from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder='.')
CORS(app)

# API kalitni environment variable'dan o'qish
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "qwen/qwen3.8-27b"

@app.route('/')
def home():
    return redirect('/index.html')

@app.route('/index.html')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/simulator.html')
def simulator():
    return send_from_directory('.', 'simulator.html')

@app.route('/flashcards.html')
def flashcards():
    return send_from_directory('.', 'flashcards.html')

@app.route('/cases.json')
def cases():
    return send_from_directory('.', 'cases.json')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_text = data.get('text', '')
        context = data.get('context', '')

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "Siz USMLE tibbiy simulyatorining tajribali professorisiz. O'zbek tilida, qisqa, aniq va tibbiy asoslab javob bering."},
                {"role": "user", "content": f"Klinik kontekst:\n{context}\n\nTalabaning savoli:\n{user_text}"}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }

        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            return jsonify({"error": f"API xatosi: {resp.status_code}"}), 500

        result = resp.json()
        if 'choices' in result and len(result['choices']) > 0:
            return jsonify({"response": result['choices'][0]['message']['content']})
        return jsonify({"error": "AI javob bermadi"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    print(f"Server: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)