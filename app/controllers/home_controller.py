from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.models.user import User  # Mengimpor model User
from app.models.post import Post  # Mengimpor model Post
from app.models.comment import Comment  # Mengimpor model Comment


from app import db  # Mengimpor instance db

def home_alone():
    username = session.get('username')
    # Mengambil semua data dari tabel User
    users = User.query.all()  # Mengambil semua data user
    posts = Post.query.order_by(Post.created_at.desc()).limit(3).all()  # Mengambil 3 postingan terbaru
    print(users)
    # Mengonversi data menjadi format yang bisa digunakan dalam template
    user_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    post_data =[{ 'id': post.id, 'title' : post.title, 'content': post.content, 'gambar' : post.image_filename ,'user_id': post.user_id,
            'username': post.user.username, 'category_name': post.category.name }for post in posts]

    home_data = {
        'title': 'Home',
        'content': 'This is the home page of the website.',
        'users': user_data,  # Menyimpan data user ke dalam home_data
        'post' : post_data
    }
    
    return render_template('pages/index.html', home_data=home_data, username=username)


