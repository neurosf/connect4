from game_logic import *
from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('play_event')
def play(data):
    request_data = data
    
    if not request_data:
        socketio.emit('response', {"error": "No data provided"})
        return

    board = request_data.get("board")
    turn = request_data.get("turn")
    mode = request_data.get("mode")
    play_col = request_data.get("play_col")
    
    if board is None or turn is None or mode is None or play_col is None:
        socketio.emit('response', {"error": "Invalid data format"})
        return
    
    state = ConnectFourBoard(board)
    err = 0
    GameState = 0
    if mode == 1:
        if turn == 1:
            play_row , err = Play.humanTurn2(state, play_col)
        elif turn == -1:
            play_row , play_col = Play.computerTurn2(state)
    else:
        if turn == 1:
            play_row , play_col = Play.computerTurn1(state)
        elif turn == -1:
            play_row , play_col = Play.computerTurn2(state)
    
    state.makeMove(play_row , play_col, turn)
    GameState = getGameState(state, turn)

    socketio.emit('response', {'board': state.board, 'GameState': GameState, 'Err': err})
    
@socketio.on('timeout_event')
def timeout(data):
    request_data = data

    if not request_data:
        socketio.emit('response', {"error": "No data provided"})
        return

    board = request_data.get("board")
    turn = request_data.get("turn")

    if board is None or turn is None:
        socketio.emit('response', {"error": "Invalid data format"})
        return

    state = ConnectFourBoard(board)
    GameState = 0
    play_row, play_col = Play.playrandom(state)

    state.makeMove(play_row, play_col, turn)
    GameState = getGameState(state, turn)

    socketio.emit('response', {'board': state.board, 'GameState': GameState, 'Err': 0})

def getGameState(state,turn):
    if state.gameOver(turn):
        if state.win(turn):
            return turn
        else :
            return 2

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    socketio.emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True,port=5000)

@app.route('/play', methods=['POST'])
def play():
    request_data = request.json
    
    if not request_data:
        return {"error": "No data provided"}, 400

    board = request_data.get("board")
    turn = request_data.get("turn")
    mode = request_data.get("mode")
    play_col = request_data.get("play_col")
    
    if board is None or turn is None or mode is None or play_col is None:
        return {"error": "Invalid data format"}, 400
    state = ConnectFourBoard(board)
    err = 0
    GameState = 0
    if mode == 1:
        if turn == 1:
            play_row , play_col = Play.computerTurn2(state)
        if turn == -1:
            play_row , err = Play.humanTurn2(state,play_col)
    else :
        if turn == 1:
            play_row , play_col = Play.computerTurn2(state)
        if turn == -1:
            play_row , play_col = Play.computerTurn2(state)
    state.makeMove(play_row , play_col,turn)
    GameState = getGameState(state,turn)

    return {"board": state.board,"GameState":GameState,"Err":err}

@app.route('/timeout', methods=['POST'])
def timeout():
    request_data = request.json
    
    if not request_data:
        return {"error": "No data provided"}, 400

    board = request_data.get("board")
    turn = request_data.get("turn")
    
    if board is None or turn is None:
        return {"error": "Invalid data format"}, 400
    state = ConnectFourBoard(board)
    GameState = 0
    play_row , play_col = Play.playrandom(state)

    state.makeMove(play_row,play_col,turn)
    GameState = getGameState(state,turn)

    return {"board": state.board,"GameState":GameState,"Err":0}

