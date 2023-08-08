from db import db


class TrainerModel(db.Model):
    __tablename__ = "trainers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False, nullable=False)
    username = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    pokemon = db.relationship("PokemonModel", back_populates="trainer", lazy="dynamic")