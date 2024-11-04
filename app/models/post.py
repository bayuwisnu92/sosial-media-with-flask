from app import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image_filename = db.Column(db.String(100), nullable=True)  # Kolom gambar baru
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    category = db.relationship('Category', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Post {self.title}>"
