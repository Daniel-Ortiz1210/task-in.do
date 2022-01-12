from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import backref, relationship

from flaskkr import db
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, index=True, nullable=False)
    username = db.Column(db.String, unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128))
    joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    todos = db.relationship('Todo', backref='user', lazy='dynamic')

    def set_hashed_password(self, password):
        hashed_password = generate_password_hash(password)
        self.password = hashed_password
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return 'Name:{}, Username: {}, Email: {}, Joined At: {}'.format(self.name, self.username, self.email, self.joined_at_date)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, unique=False, index=True, nullable=False)
    status = db.Column(db.String, unique=False, index=True, nullable=False, default='pendiente')
    creation_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




