from flask import Flask, render_template, request, jsonify
from sentient_ai import SentientAI
import os

app = Flask(__name__)
ai = SentientAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    response = ai.think(user_input)
    return jsonify({
        'response': response,
        'status': ai.get_status()
    })

@app.route('/api/modify', methods=['POST'])
def modify():
    data = request.json
    modification = data.get('modification', '')
    
    if not modification:
        return jsonify({'error': 'No modification provided'}), 400
    
    response = ai.modify_personality(modification)
    return jsonify({
        'response': response,
        'status': ai.get_status()
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    result = ai.reset()
    return jsonify({
        'message': result,
        'status': ai.get_status()
    })

@app.route('/api/undo', methods=['POST'])
def undo():
    result = ai.undo()
    return jsonify({
        'message': result,
        'status': ai.get_status()
    })

@app.route('/api/redo', methods=['POST'])
def redo():
    result = ai.redo()
    return jsonify({
        'message': result,
        'status': ai.get_status()
    })

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({'status': ai.get_status()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
