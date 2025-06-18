
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_session import Session
from flask_socketio import SocketIO
from redis_manager import RedisManager
import redis

redis_db = redis.StrictRedis(host='localhost', port=6379)
# redis_db = redis.StrictRedis(host='172.20.0.10', port=6379)
redis_manager = RedisManager(redis_db)

class DevConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = b'L\x1eR\xf5\xfb0T~\t+\xde\x9b\xef\xcb\xfd\xff'

    # Redis
    SESSION_TYPE = 'redis' # default is filesystem
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = False
    SESSION_KEY_PREFIX = 'session:'
    SESSION_REDIS = redis_db

app = Flask(__name__)

app.config.from_object(DevConfig())
Session(app)
CORS(app, supports_credentials=True)

app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)
