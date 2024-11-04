from flask import render_template, session, redirect, url_for, flash, request, current_app

from app.models.post import Post
from werkzeug.utils import secure_filename
from app.models.category import Category
from app import db,create_app
from datetime import datetime
import os
from app.models.user import User

from app.forms import PostForm



def index():
    if 'user_id' not in session:
        flash('Anda sudah login!', 'info')
        return redirect(url_for('main.login'))
    
    # Ambil hanya post yang dibuat oleh user yang sedang login
    posts = Post.query.filter_by(user_id=session['user_id']).all()
    nama = session.get('username')

    post_data = [
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'user_id': post.user_id,
            'username': post.user.username,  # Mendapatkan username dari user terkait
            'category_id': post.category_id,
            'category_name': post.category.name  # Mendapatkan nama kategori
        }
        for post in posts
    ]
    return render_template('dashboard/dashboard.html', posts=post_data, nama=nama)

def create_post():
    form = PostForm()

    # Ambil semua kategori dari database
    categories = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]

    if 'user_id' not in session:
        flash('Anda harus login terlebih dahulu untuk membuat post.', 'warning')
        return redirect(url_for('main.login'))

    if form.validate_on_submit():
        # Proses gambar
        image_filename = None
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.root_path, 'static/uploads', image_filename))


        post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=session['user_id'],
            category_id=form.category.data,
            image_filename=image_filename,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(post)
        db.session.commit()
        flash('Post berhasil dibuat!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('dashboard/create_post.html', form=form)


def update_post(post_id):
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'info')
        return redirect(url_for('main.login'))

    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    categories = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category_id = form.category.data

        # Update gambar jika ada file baru yang diunggah
        if form.image.data:
            image_file = form.image.data
            image_filename = secure_filename(image_file.filename)
            # Menggunakan config untuk folder upload
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
            post.image_filename = image_filename  # Update nama file gambar pada post

        db.session.commit()
        flash('Post berhasil diupdate!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('dashboard/update_post.html', post=post, form=form)


def delete_post(post_id):
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'info')
        return redirect(url_for('main.login'))
    
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    flash('Post berhasil dihapus!', 'success')
    return redirect(url_for('main.dashboard'))

    
