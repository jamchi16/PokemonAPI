from marshmallow import Schema, fields

class PlainPokemonSchema(Schema):
    id = fields.Int(dump_only=True)
    species = fields.Str(required=True)
    nickname = fields.Str(required=True)
    level = fields.Int(required=True)
    trade_status = fields.Boolean(required=True)

class PlainTrainerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=False)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    pokemon = fields.List(fields.Nested(PlainPokemonSchema()), dump_only=True)

class PokemonSchema(PlainPokemonSchema):
    trainer_id = fields.Int(required=True, load_only=True)
    trainer = fields.Nested(PlainTrainerSchema(only=("name",)), dump_only=True)

class PokemonUpdateSchema(Schema):
    nickname = fields.Str()
    trainer_id = fields.Int()
    trade_status = fields.Boolean()

class TrainerSchema(PlainTrainerSchema):
    pokemon = fields.List(fields.Nested(PlainPokemonSchema()), dump_only=True)

