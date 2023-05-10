from app import db
import datetime
from flask_login import UserMixin

class Account(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def get_id(self):
        return str(self.id)
    
    def __init__(self, username, password, is_admin=False, is_active=True):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.is_active = is_active
        
    def serialize(self):
        return {
            "username": self.username,
            "is_admin": self.is_admin,
            "is_active": self.is_active
        }
