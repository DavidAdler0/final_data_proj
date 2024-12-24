from db import db


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    latitude = db.Column(db.String, nullable=True)
    longitude = db.Column(db.String, nullable=True)
    terror_event = db.Relationship('TerrorEvent', back_populates='location')