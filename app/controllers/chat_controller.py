from flask import render_template, request, session, redirect, url_for, flash
from app.models.chat import Chat


def chat():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))  # Ganti dengan rute login yang sesuai

    # Ambil semua chat yang ada di room chat umum
    chats = Chat.query.order_by(Chat.timestamp).all()

    # Buat data room untuk template
    

    return render_template('pages/chat.html', chats=chats)