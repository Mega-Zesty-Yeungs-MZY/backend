from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


class Leaderboards(db.Model):
    __tablename__ = 'Leaderboards' 

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=True, nullable=False)
    _time = db.Column(db.String(255), unique=True, nullable=False)
    def __init__(self, name, time):
        self._time = time   
        self._name = name

    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, time):
        self._time = time

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
            "time": self.time,
            "name": self.name,
            
        }

# UPDATE

    def update(self, time="", name=""):
        if len(time) > 0:
            self.time = time
        if len(name) > 0:
            self.name = name
        db.session.commit()
        return self

# DELETE

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initLeaderboards():
    with app.app_context():
        db.create_all()
        u1 = Leaderboards( time='100000000 sec', name='Dillon' )
        u2 = Leaderboards( time='100000001 sec', name='Steven' )
        u3 = Leaderboards( time='100000002 sec', name='Noor' )
        u4 = Leaderboards( time='100000003 sec', name='Lucas' )
        u5 = Leaderboards( time='100000004', name='Yeung' )

        entries = [u1, u2, u3, u4, u5]

        for entry in entries:
            try:
                entry.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate email, or error:")

    