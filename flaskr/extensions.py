from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    miner = db.relationship('Miner', backref='user', lazy=True)

    def __repr__(self):
        return f"""
        id: {self.id}
        username: {self.username}
        created_date: {self.created_at}
    """

class Miner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    enabled = db.Column(db.Boolean,  nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    created_user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    def __repr__(self):
        return f"""
        id: {self.id}
        name: {self.name}
        enabled: {self.enabled}
        created_date: {self.created_at}
        created_user_id: {self.created_user_id}
    """