from db import db
from sqlalchemy import Boolean

class PokemonModel(db.Model):
    __tablename__ = "pokemon"

    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(256), unique=False, nullable=False)
    nickname = db.Column(db.String(256), unique=True, nullable=True)
    level = db.Column(db.Integer, unique=False, nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainers.id"), unique=False, nullable=False)
    trainer = db.Relationship("TrainerModel", back_populates="pokemon")
    trade_status = db.Column(Boolean, unique=False)