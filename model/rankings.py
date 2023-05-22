from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


class Charges(db.Model):
    __tablename__ = 'Charges' 

    id = db.Column(db.Integer, primary_key=True)
    _car = db.Column(db.String(255), unique=True, nullable=False)
    _chargetime = db.Column(db.String(255), unique=True, nullable=False)
    def __init__(self, car, chargetime):
        self._chargetime = chargetime   
        self._car = car

    @property
    def chargetime(self):
        return self._chargetime
    
    @chargetime.setter
    def chargetime(self, chargetime):
        self._chargetime = chargetime

    @property
    def car(self):
        return self._car

    @car.setter
    def car(self, car):
        self._car = car

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
            "chargetime": self.chargetime,
            "car": self.car,
            
        }

# UPDATE

    def update(self, chargetime="", car=""):
        if len(chargetime) > 0:
            self.chargetime = chargetime
        if len(car) > 0:
            self.car = car
        db.session.commit()
        return self

# DELETE

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initCharges():
    with app.app_context():
        db.create_all()
        u1 = Charges( chargetime='Around 10 Hours', car='Lucid Air' )
        u2 = Charges( chargetime='Around 7 Hours', car='Tesla Model X' )
        u3 = Charges( chargetime='Around 7 Hours', car='Tesla Model S' )
        u4 = Charges( chargetime='Around 18 Hours', car='Rivian R1T' )
        u5 = Charges( chargetime='Around 11 Hours', car='NIO ET5' )

        charges = [u1, u2, u3, u4, u5]

        for charge in charges:
            try:
                charge.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate email, or error:")

    