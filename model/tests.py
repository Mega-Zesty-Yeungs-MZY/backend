from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


class Rankings(db.Model):
    __tablename__ = 'Rankings' 

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=True, nullable=False)
    _score = db.Column(db.String(255), unique=True, nullable=False)
    def __init__(self, name, score):
        self._score = score 
        self._name = name

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, score):
        self._score = score

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __str__(self):
        return json.dumps(self.read())

# CREATE

    def create(self):
        try:
            db.session.add(self)  
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

# READ

    def read(self):
        return {
            "id": self.id,
            "score": self.score,
            "name": self.name,
            
        }

# UPDATE

    def update(self, score="", name=""):
        if len(score) > 0:
            self.score = score
        if len(name) > 0:
            self.name = name
        db.session.commit()
        return self

# DELETE

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initRankings():
    with app.app_context():
        db.create_all()
        u1 = Rankings( score='100000000 sec', name='Dillon' )
        u2 = Rankings( score='100000001 sec', name='Steven' )
        u3 = Rankings( score='100000002 sec', name='Noor' )
        u4 = Rankings( score='100000003 sec', name='Lucas' )
        u5 = Rankings( score='100000004 sec', name='Yeung' )

        scores = [u1, u2, u3, u4, u5]

        for score in scores:
            try:
                score.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate email, or error:")

    