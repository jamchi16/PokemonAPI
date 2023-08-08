from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt, get_jwt_identity
from blocklist import BLOCKLIST

from db import db
from models import TrainerModel
from schemas import TrainerSchema

blp = Blueprint("Trainers", "trainers", description="Operations on trainers")

@blp.route("/register")
class TrainerRegister(MethodView):
    @blp.arguments(TrainerSchema)
    def post(self, trainer_data):
        if TrainerModel.query.filter(TrainerModel.username == trainer_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        trainer = TrainerModel(
            name=trainer_data["name"],
            username=trainer_data["username"],
            password=pbkdf2_sha256.hash(trainer_data["password"]),
        )
        db.session.add(trainer)
        db.session.commit()

        return {"message": "Trainer created successfully."}, 201

@blp.route("/trainer/<int:trainer_id>")
class Trainer(MethodView):
    @blp.response(200, TrainerSchema)
    def get(self, trainer_id):
        trainer = TrainerModel.query.get_or_404(trainer_id)
        return trainer

    @jwt_required()
    def delete(self, trainer_id):
        trainer = TrainerModel.query.get_or_404(trainer_id)
        for pokemon in trainer.pokemon:
            db.session.delete(pokemon)
        
        db.session.delete(trainer)
        db.session.commit()
        return {"message": "Trainer deleted."}, 200

@blp.route("/login")
class TrainerLogin(MethodView):
    @blp.arguments(TrainerSchema)
    def post(self, trainer_data):
        trainer = TrainerModel.query.filter(
            TrainerModel.username == trainer_data["username"]
        ).first()

        if trainer and pbkdf2_sha256.verify(trainer_data["password"], trainer.password):
            access_token = create_access_token(identity=trainer.id)
            return{"access_token": access_token}
        abort(401, message="Invalid Credentials.")

@blp.route("/logout")
class TrainerLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}
