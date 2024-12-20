from app import db, app


class Player(db.Model):
    __tablename__ = 'players'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    sid = db.Column(db.String(100), unique=True, nullable=False)  # Идентификатор сокета
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)

    room = db.relationship('Room', back_populates='players')

    def __repr__(self):
        return f'<Player {self.username}>'


class Room(db.Model):
    __tablename__ = 'rooms'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    players = db.relationship('Player', back_populates='room', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Room {self.name}>'


class Boat(db.Model):
    __tablename__ = 'boats'  # Изменено на 'boats'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)  # Исправлено на 'players.id'
    room_id = db.Column(db.String(50), db.ForeignKey('rooms.id'), nullable=False)
    row_index = db.Column(db.Integer, nullable=False)
    cell_index = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    is_horizontal = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Boat {self.player_id} {self.row_index} {self.cell_index} {self.size} {self.is_horizontal}>'





with app.app_context():
    db.drop_all()  # Удаляет все таблицы
    db.create_all()  # Создает все таблицы заново
