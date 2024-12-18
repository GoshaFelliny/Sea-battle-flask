from flask import Flask
from flask_socketio import SocketIO
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes
