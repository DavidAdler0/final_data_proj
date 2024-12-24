from db import db


class TerrorEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, nullable=True)
    month = db.Column(db.Integer, nullable=True)
    day = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    terror_group = db.Column(db.String, nullable=True)
    kills = db.Column(db.Integer, nullable=True)
    wounds = db.Column(db.Integer, nullable=True)
    attack_type = db.Column(db.String, nullable=True)
    weapon_type = db.Column(db.String, nullable=True)
    target_type = db.Column(db.String, nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.Relationship('Location', back_populates='terror_event')
