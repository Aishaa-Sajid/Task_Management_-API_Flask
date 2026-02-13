from app import db
from datetime import datetime

class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    description=db.Column(db.String(300))
    status=db.Column(db.String(20))
    priority=db.Column(db.String(20))
    due_date=db.Column(db.String(20))

    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    category_id=db.Column(db.Integer,db.ForeignKey("category.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)