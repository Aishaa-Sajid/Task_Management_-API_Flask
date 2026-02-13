from app import db 
from datetime import datetime

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100),unique=True, nullable=False)
    username=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)