from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import PokemonSchema, PokemonUpdateSchema
from models import PokemonModel
from db import db
from flask_jwt_extended import jwt_required
from flask import jsonify

blp = Blueprint("Pokemon", "pokemon", description="Operations on pokemon")

@blp.route("/pokemon/<int:pokemon_id>")
class Pokemon(MethodView):
    @jwt_required()
    @blp.response(200, PokemonSchema)
    def get(self, pokemon_id):
        pokemon = PokemonModel.query.get_or_404(pokemon_id)
        return pokemon

    @jwt_required()
    def delete(self, pokemon_id):
        pokemon = PokemonModel.query.get_or_404(pokemon_id)
        db.session.delete(pokemon)
        db.session.commit()
        return {"message": "Pokemon deleted."}
    
    @jwt_required()
    @blp.arguments(PokemonUpdateSchema)
    @blp.response(200, PokemonSchema)
    def put(self, pokemon_data, pokemon_id):
        pokemon = PokemonModel.query.get(pokemon_id)

        if pokemon:
            pokemon.nickname = pokemon_data["nickname"]
            pokemon.trade_status = pokemon_data["trade_status"]
            pokemon.trainer_id = pokemon_data["trainer_id"]
        else:
            pokemon = PokemonModel(id=pokemon_id, **pokemon_data)

        db.session.add(pokemon)
        db.session.commit()

        return pokemon

@blp.route("/pokemon")
class PokemonList(MethodView):
    @blp.arguments(PokemonSchema)
    @blp.response(201, PokemonSchema)
    def post(self, pokemon_data):
        pokemon = PokemonModel(**pokemon_data)

        try:
            db.session.add(pokemon)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return pokemon

    @jwt_required()
    @blp.response(200, PokemonSchema(many=True))
    def get(self):
        return PokemonModel.query.all()
    
