from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    comments = db.relationship('Comment', back_populates='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Menyimpan waktu pembuatan
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Waktu pembaruan

    def __repr__(self):
        return f"<User {self.username}>"
