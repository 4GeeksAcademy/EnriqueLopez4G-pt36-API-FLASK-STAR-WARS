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
from models import db, User,Character,Planet,Favorite

#---------------------
#LAS RUTAS QUE PRETENDO CREAR MAS ADELANTE

    #GET /people
    #GET /people/int

    #GET /planets
    #GET /planets/int:planet_id

    #GET /users
    #GET /users/favorites

    #POST /favorite/planet/int:planet_id
    #POST /favorite/people/int:people_id
    #DELETE /favorite/planet/int:planet_id
    #DELETE /favorite/people/int:people_id

#---------------------

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
#---------------------------------------


@app.route('/people', methods=['GET'])
def get_all_people():
    characters = Character.query.all()  # Obtiene todos los personajes
    return jsonify([char.serialize() for char in characters]), 200
#-----------------------------------------------------------------
@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    character = Character.query.get_or_404(people_id)  # Obtiene el personaje o 404 si no existe
    return jsonify(character.serialize()), 200
#------------------------------------------------
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()  # Obtiene todos los planetas
    return jsonify([planet.serialize() for planet in planets]), 200
#------------------------------------------------------------------
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)  # Obtiene el planeta o 404 si no existe
    return jsonify(planet.serialize()), 200

#-------------------------------------------
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()  # Obtiene todos los usuarios
    return jsonify([user.serialize() for user in users]), 200
#------------------------------------------------------------
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # Para este ejemplo, asumimos que el usuario con id = 1 está autenticado
    user_id = 1  # Esto debe cambiar cuando se implemente autenticación
    user = User.query.get_or_404(user_id)
    
    # Obtiene todos los favoritos del usuario
    favorites = [favorite.serialize() for favorite in user.favorites]
    return jsonify(favorites), 200
#--------------------------------------------------------------
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  # Esto debe cambiar cuando se implemente autenticación
    user = User.query.get_or_404(user_id)
    planet = Planet.query.get_or_404(planet_id)
    
    # Crear un nuevo favorito
    favorite = Favorite(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": f"Planet {planet.name} added to favorites."}), 201
#------------------------------------------------------------------------------
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user_id = 1  # Esto debe cambiar cuando se implemente autenticación
    user = User.query.get_or_404(user_id)
    character = Character.query.get_or_404(people_id)
    
    # Crear un nuevo favorito
    favorite = Favorite(user_id=user.id, character_id=character.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": f"Character {character.name} added to favorites."}), 201
#----------------------------------------------------------------------------------
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user_id = 1  # Esto debe cambiar cuando se implemente autenticación
    user = User.query.get_or_404(user_id)
    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Planet removed from favorites."}), 200
    return jsonify({"msg": "Favorite not found."}), 404
#---------------------------------------------------------------------
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_person(people_id):
    user_id = 1  # Esto debe cambiar cuando se implemente autenticación
    user = User.query.get_or_404(user_id)
    favorite = Favorite.query.filter_by(user_id=user.id, character_id=people_id).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Character removed from favorites."}), 200
    return jsonify({"msg": "Favorite not found."}), 404





#---------------------------------------
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
