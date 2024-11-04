from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_socketio import SocketIO

import os

load_dotenv()

# Inisialisasi di ruang lingkup global
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()  # Memindahkan bcrypt ke sini
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    UPLOAD_FOLDER = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')


    # Inisialisasi ekstensi dengan aplikasi
    db.init_app(app)
    bcrypt.init_app(app)  # Inisialisasi bcrypt di sini
    migrate.init_app(app, db)
    socketio.init_app(app)
    

    # Register blueprint dan model dalam app context
    with app.app_context():
        from .routes import main  # Mengimpor Blueprint dari routes
        from .models.category import Category
        from .models.user import User
        from .models.post import Post
        from .models.comment import Comment
        from .models.chat import Chat
        from .models.chatroom import ChatRoom
        from .models.ChatRoomUser import ChatRoomUser

        app.register_blueprint(main)  # Pastikan blueprint bernama 'main' di routes

        # Membuat semua tabel jika belum ada
        db.create_all()

    return app
