from app import app, socketio, db
from flask import render_template, request
from flask_socketio import emit
import uuid
import random
from app.model import Player, Room


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game/<game_id>')
def game(game_id):
    room = Room.query.get(game_id)

    players = room.players if room else []
    rows = range(1, 11)  # Номера строк от 1 до 10
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']  # Буквы столбцов
    return render_template('game.html', game_id=game_id, players=players, rows=rows, columns=columns)


@socketio.on('create_game')
def create_game():
    game_id = str(uuid.uuid4())
    new_room = Room(id=game_id, name=f'Game {game_id}')
    db.session.add(new_room)
    db.session.commit()

    # Добавляем первого игрока
    new_player = Player(username=request.sid, sid=request.sid, room_id=new_room.id)
    db.session.add(new_player)
    db.session.commit()

    emit('game_created', {'game_id': game_id}, broadcast=False)
    print('Игра создана', game_id, 'игроком', new_player.username)


@socketio.on('find_game')
def find_game():
    available_rooms = Room.query.filter(Room.players.any()).all()
    available_games = [room.id for room in available_rooms if len(room.players) < 2]

    if available_games:
        # Выбираем случайную игру из доступных
        game_id = random.choice(available_games)
        print(f'Найдена игра: {game_id}')  # Отладочное сообщение
        emit('game_found', {'game_id': game_id}, broadcast=False)

        # Добавляем игрока в комнату
        room = Room.query.get(game_id)
        new_player = Player(username=request.sid, sid=request.sid, room_id=room.id)
        db.session.add(new_player)
        db.session.commit()

        print('Игрок подключен:', request.sid)
        emit('player_joined', {'player_id': request.sid}, room=game_id)

        # Если это второй игрок, уведомляем обоих игроков
        if len(room.players) == 2:
            print('Игра может быть запущена')
            emit('game_start', {'message': 'Игра началась!', 'game_id': game_id}, room=game_id)
    else:
        print('Игры не найдены')  # Отладочное сообщение
        emit('game_found', {'game_id': None}, broadcast=False)  # Если игр нет
