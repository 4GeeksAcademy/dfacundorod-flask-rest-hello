"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favorite_character, Favorite_planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = list(map(lambda usuario: usuario.serialize(), all_users))
    return jsonify(result), 200

@app.route('/user/<int:user_id>',  methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return {'Message': 'User not found!'}
    result = user.serialize()
    return jsonify(result), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    result = list(map(lambda planet: planet.serialize(), all_planets))
    return jsonify(result), 200

@app.route('/planet/<int:planet_id>',  methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    if planet is None:
        return {'Message': 'User not found!'}
    result = planet.serialize()
    return jsonify(result), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = Characters.query.all()
    result = list(map(lambda character: character.serialize(), all_characters))
    return jsonify(result), 200

@app.route('/characters/<int:character_id>',  methods=['GET'])
def get_character(character_id):
    character = Characters.query.filter_by(id=character_id).first()
    if character is None:
        return {'Message': 'User not found!'}
    result = character.serialize()
    return jsonify(result), 200


@app.route('/user/favorites_planets', methods=['GET'])
def get_favorites():
    all_favorites = Favorite_planet.query.all()
    result = list(map(lambda favorite: favorite.serialize(), all_favorites))
    return jsonify(result)
    

@app.route('/favorites/planet/<int:planet_id>' ,methods=['POST'])
def create_favorite_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    if planet is None:
        return {'message': 'Planet not found'}, 404
    new_planet_favorite = Favorite_planet(user_id=1 , planet_id=planet_id )
    db.session.add(new_planet_favorite)
    db.session.commit()
    return {'message': 'Planet added'}

@app.route('/favorites/planet/<int:planet_id>' ,methods=['DELETE'])
def delete_favorite_planet(planet_id):
    planet = Favorite_planet.query.filter_by(id=planet_id).first()
    if planet is None:
        return {'message': 'Planet not found'}, 404
    db.session.delete(planet)
    db.session.commit()
    return {'message': 'Planet deleted'}

@app.route('/user/Favorite_character', methods=['GET'])
def create_character():
    all_favorites = Favorite_character.query.all()
    result = list(map(lambda favorite: favorite.serialize(), all_favorites))
    return jsonify(result)

@app.route('/favorites/character/<int:character_id>' ,methods=['POST'])
def create_favorite_character(character_id):
    character = Characters.query.filter_by(id=character_id).first()
    if character is None:
        return {'message': 'Character not found'}, 404
    new_character_favorite = Favorite_character(user_id=1 , character_id=character_id )
    db.session.add(new_character_favorite)
    db.session.commit()
    return {'message': 'Character added'}

@app.route('/favorites/character/<int:character_id>' ,methods=['DELETE'])
def delete_favorite_character(character_id):
    character = Favorite_character.query.filter_by(id=character_id).first()
    if character is None:
        return {'message': 'Planet not found'}, 404
    db.session.delete(character)
    db.session.commit()
    return {'message': 'Character deleted'}




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
