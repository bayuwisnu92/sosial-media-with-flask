from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.controllers.profile_controller import get_user_profile, post_detail, author_route_route, category_category_route
from app.controllers.dashboard_controller import index, create_post, update_post, delete_post
from app.controllers.auth_controller import index_register, index_login, index_logout
from app.controllers.home_controller import home_alone
from app.controllers.chat_controller import chat
from app.models.chatroom import ChatRoom

from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User
from app.models.chat import Chat
from app import db
from app import socketio
from flask import jsonify
from datetime import datetime

from flask_socketio import emit

main = Blueprint('main', __name__)

@main.route('/')
def home():  
    return home_alone()

@main.route('/post')
def profile():
    return get_user_profile()

@main.route('/dashboard')
def dashboard():
    return index()

@main.route('/register', methods=['GET', 'POST'])
def register():
    return index_register()

@main.route('/login', methods=['GET', 'POST'])
def login():
    return index_login()

@main.route('/logout')
def logout():
    return index_logout()

@main.route('/create_post', methods=['GET', 'POST'])
def create_post_route():
    return create_post()

@main.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
def update_post_route(post_id):
    return update_post(post_id)

@main.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post_route(post_id):
    return delete_post(post_id)

@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail_route(post_id):
    return post_detail(post_id)

@main.route('/author/<username>')
def author_route(username):
    return author_route_route(username)

@main.route('/category/<category_name>')
def category_route(category_name):
    return category_category_route(category_name)

@main.route('/chat')
def chat_route():
    return chat()


@socketio.on('send_message')
def handle_message(data):
    user_id = session.get('user_id')  # Ambil ID user dari session
    username = session.get('username')  # Ambil username dari session
    message_content = data['message']
    
    # Simpan ke database dengan nama kolom yang benar
    chat = Chat(user_id=user_id, message=message_content)
    db.session.add(chat)
    db.session.commit()
    
    # Format timestamp menjadi string
    formatted_timestamp = chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    # Emit pesan ke semua pengguna dengan username pengirim
    emit('receive_message', {'username': username, 'message': message_content, 'timestamp': formatted_timestamp}, broadcast=True)


@main.route('/chat/history')
def chat_history():
    # Ambil 50 pesan terakhir dari database
    messages = Chat.query.order_by(Chat.timestamp.desc()).limit(50).all()
    
    # Format data untuk dikirim ke frontend
    messages_data = [
        {'username': msg.user.username, 'message': msg.message, 'timestamp': msg.timestamp}
        for msg in messages
    ]
    return jsonify(messages_data)

# membuat chat personal

@main.route('/create_chatroom', methods=['GET', 'POST'])
def create_chatroom():
    if request.method == 'POST':
        room_name = request.form['room_name']
        new_chatroom = ChatRoom(room_name=room_name)
        db.session.add(new_chatroom)
        db.session.commit()
        return redirect(url_for('main.chatrooms'))  # Redirect ke daftar chatroom

    return render_template('chatroom/create_chatroom.html')

@main.route('/chatrooms')
def chatrooms():
    chatrooms = ChatRoom.query.all()
    return render_template('chatroom/chatrooms.html', chatrooms=chatrooms)


@main.route('/personal_chat/<int:room_id>')
def personal_chat(room_id):
    chatroom = ChatRoom.query.get_or_404(room_id)
    chats = Chat.query.filter_by(room_id=room_id).order_by(Chat.timestamp).all()
    return render_template('chatroom/personal_chat.html', chatroom=chatroom, chats=chats)

@main.route('/send_personal_chat/<int:room_id>', methods=['POST'])
def send_personal_chat(room_id):
    chatroom = ChatRoom.query.get_or_404(room_id)
    message_content = request.form.get('message')
    
    if message_content:
        new_chat = Chat(user_id=session['user_id'], room_id=room_id, message=message_content)
        db.session.add(new_chat)
        db.session.commit()
    
    return redirect(url_for('main.personal_chat', room_id=room_id))

@socketio.on('send_message')
def handle_send_message(data):
    room_id = data['room_id']
    message = data['message']
    username = data['username']
    user_id = data['user_id']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Kirim pesan ke room agar semua klien di room tersebut menerima pesan
    emit('receive_message', {
        'username': username,
        'message': message,
        'timestamp': timestamp,
        'user_id': user_id
    }, room=room_id)

    # Simpan pesan ke database jika diperlukan
    new_chat = Chat(room_id=room_id, user_id=user_id, message=message, timestamp=timestamp)
    db.session.add(new_chat)
    db.session.commit()