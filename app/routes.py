from app import app, socketio
from flask import render_template, request
from flask_socketio import emit
import uuid
import random

rooms = {}  #текущие сессии


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game/<game_id>')
def game(game_id):
    players = rooms.get(game_id, {}).get('players', [])
    return render_template('game.html', game_id=game_id, players=players)


@socketio.on('create_game')
def create_game():
    game_id = str(uuid.uuid4())
    rooms[game_id] = {'players': [], 'board': []}  # Здесь можно хранить состояние игры
    rooms[game_id]['players'].append(request.sid)
    emit('game_created', {'game_id': game_id}, broadcast=False)
    print('Игра создана', game_id)


@socketio.on('find_game')
def find_game():
    available_games = [game_id for game_id in rooms if len(rooms[game_id]['players']) < 2]
    if available_games:
        # Выбираем случайную игру из доступных
        game_id = random.choice(available_games)
        print(f'Найдена игра: {game_id}')  # Отладочное сообщение
        emit('game_found', {'game_id': game_id}, broadcast=False)

        # Добавляем игрока в комнату
        rooms[game_id]['players'].append(request.sid)
        print('Игрок подключен:', request.sid)
        emit('player_joined', {'player_id': request.sid}, room=game_id)

        # Если это второй игрок, уведомляем обоих игроков
        if len(rooms[game_id]['players']) == 2:
            print('Игра может быть запущена')
            emit('game_start', {'message': 'Игра началась!', 'game_id': game_id}, room=game_id)
    else:
        print('Игры не найдены')  # Отладочное сообщение
        emit('game_found', {'game_id': None}, broadcast=False)  # Если игр нет


