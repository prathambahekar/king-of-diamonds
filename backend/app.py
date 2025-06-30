from flask import Flask, request, jsonify, send_from_directory
from .games import Game
import os

app = Flask(__name__)

game_instance = None

@app.route('/api/start', methods=['POST'])
def start_game():
    global game_instance
    num_ai = request.json.get('num_ai', 4)
    game_instance = Game(num_ai=num_ai)
    return jsonify({'status': 'started'})

@app.route('/api/state', methods=['GET'])
def get_state():
    global game_instance
    if not game_instance:
        return jsonify({'error': 'No game started'}), 400
    # You may need to add a method to Game to serialize its state
    return jsonify(game_instance.serialize())

@app.route('/api/play', methods=['POST'])
def play_move():
    global game_instance
    if not game_instance:
        return jsonify({'error': 'No game started'}), 400
    move = request.json.get('move')
    # You may need to implement a method to process a move
    result = game_instance.play_move(move)
    return jsonify(result)

@app.route('/api/history', methods=['GET'])
def get_history():
    global game_instance
    if not game_instance:
        return jsonify([])
    return jsonify(game_instance.get_history())

@app.route('/')
def serve_index():
    return send_from_directory(os.path.join('..', 'frontend', 'webui'), 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join('..', 'frontend', 'webui'), path)

if __name__ == '__main__':
    app.run(debug=True) 