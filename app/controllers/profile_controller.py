# app/controllers/profile_controller.py

from flask import render_template, request, session, redirect, url_for, flash
from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User
from app.models.category import Category
from app import db

def get_user_profile():
    # Query semua post dengan relasi `user` dan `category`
    posts = Post.query.all()
    post_data = [
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'user_id': post.user_id,
            'gambar' : post.image_filename,

            'username': post.user.username,  # Mendapatkan username dari user terkait
            'category_id': post.category_id,
            'category_name': post.category.name  # Mendapatkan nama kategori
        }
        for post in posts
    ]

    # Data profil untuk ditampilkan di halaman
    profile_data = {
        'title': 'Post',
        'name': 'Bayu Wisnu Aji',
        'age': 25,
        'job': 'Software Developer',
        'posts': post_data
    }

    return render_template('pages/posts.html', profile=profile_data)

def post_detail(post_id):
    # Dapatkan postingan berdasarkan ID
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()

    # Jika pengguna mengirimkan komentar
    if request.method == 'POST':
        if 'user_id' in session:  # Periksa apakah pengguna sudah login
            content = request.form['content']
            if content:
                # Tambahkan komentar ke database
                comment = Comment(content=content, post_id=post.id, user_id=session['user_id'])
                db.session.add(comment)
                db.session.commit()
                flash('Komentar berhasil ditambahkan.', 'success')
                return redirect(url_for('main.post_detail_route', post_id=post.id))  # Pastikan ini
            else:
                flash('Komentar tidak boleh kosong.', 'warning')
        else:
            flash('Anda harus login untuk mengomentari.', 'danger')
            return redirect(url_for('index_login'))

    return render_template('pages/post_detail.html', post=post, comments=comments)

def author_route_route(username):
    # Mendapatkan user berdasarkan username
    user = User.query.filter_by(username=username).first()
    
    # Memastikan user ditemukan
    if not user:
        return "User tidak ditemukan", 404
    
    # Mendapatkan semua postingan dari user tersebut
    posts = Post.query.filter_by(user_id=user.id).all()
    
    # Mengambil data postingan
    post_data = [
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'user_id': post.user_id,
            'username': post.user.username,
            'gambar': post.image_filename,
            'category_id': post.category_id,
            'category_name': post.category.name  # Nama kategori dari relasi
        }
        for post in posts
    ]

    # Data profil untuk ditampilkan di halaman
    profile_data = {
        'title': 'Post oleh ' + user.username,
        'name': user.username,
        'age': 25,  # ini bisa disesuaikan dengan atribut yang ada
        'job': 'Software Developer',
        'posts': post_data
    }

    return render_template('pages/posts.html', profile=profile_data)

def category_category_route(category_name):
    # Mengambil data kategori berdasarkan nama
    category = Category.query.filter_by(name=category_name).first()

    # Memastikan kategori ditemukan
    if not category:
        return "Kategori tidak ditemukan", 404

    # Mendapatkan semua postingan dalam kategori tersebut
    posts = Post.query.filter_by(category_id=category.id).all()

    # Mengambil data postingan
    post_data = [
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'user_id': post.user_id,
            'username': post.user.username,
            'gambar': post.image_filename,
            'category_id': post.category_id,
            'category_name': category.name  # Nama kategori dari relasi
        }
        for post in posts
    ]

    # Data profil untuk ditampilkan di halaman
    profile_data = {
        'title': 'Post dalam kategori ' + category.name,
        'name': category.name,
        'posts': post_data
    }

    return render_template('pages/posts.html', profile=profile_data)