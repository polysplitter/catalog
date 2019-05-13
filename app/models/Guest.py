#!/usr/bin/env python3

from app import db

class Guest(db.Model):
    """Stores user info"""
    __tablename__ = 'guest'

    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    picture = db.Column(db.String(250))
    id = db.Column(db.Integer, primary_key=True)

    @property
    def serialize(self):
        """Return User object data in easily serializable format"""
        return {
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'id': self.id
        }
