from app import app, socketio
from flask import render_template
from flask_socketio import emit
import uuid
import random

rooms = {}  #текущие сессии


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game/<game_id>')
def game(game_id):
    return render_template('game.html', game_id=game_id)


@socketio.on('create_game')
def create_game():
    game_id = str(uuid.uuid4())
    rooms[game_id] = {'players': [], 'board': []}  # Здесь можно хранить состояние игры
    emit('game_created', {'game_id': game_id}, broadcast=False)


@socketio.on('find_game')
def find_game():
    if rooms:
        # Выбираем случайную игру из существующих
        game_id = random.choice(list(rooms.keys()))
        print(f'Найдена игра: {game_id}')  # Отладочное сообщение
        emit('game_found', {'game_id': game_id}, broadcast=False)
    else:
        print('Игры не найдены')  # Отладочное сообщение
        emit('game_found', {'game_id': None}, broadcast=False)  # Если игр нет
