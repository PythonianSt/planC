from flask import Flask, request, jsonify, send_from_directory
from fuzzywuzzy import fuzz
import json

app = Flask(__name__)

# Load FAQ data
with open('faq.json', 'r', encoding='utf-8') as f:
    faq_data = json.load(f)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')

    # Find best match
    best_score = 0
    best_answer = "ขออภัย ไม่พบคำตอบที่ตรงกับคำถามของคุณ"

    for q, a in faq_data.items():
        score = fuzz.token_set_ratio(question, q)
        if score > best_score:
            best_score = score
            best_answer = a

    return jsonify({'answer': best_answer})

if __name__ == '__main__':
    app.run(debug=True)
