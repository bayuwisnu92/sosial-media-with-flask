from app import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    posts = db.relationship('Post', back_populates='category', lazy=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Menambahkan kolom created_at
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Menambahkan kolom updated_at

    def __repr__(self):
        return f"<Category {self.name}>"