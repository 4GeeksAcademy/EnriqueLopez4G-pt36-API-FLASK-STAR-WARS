"""
Este módulo se encarga de arrancar el servidor API, cargar la DB y agregar los endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite

#---------------------
# LAS RUTAS QUE VOY A CREAR MÁS ADELANTE
# 1.- GET /people
# 2.- GET /people/int

# 3.- GET /planets
# 4.- GET /planets/int:planet_id

# 5.- GET /users
# 6.- GET /users/favorites

# 7.- POST /favorite/planet/int:planet_id
# 8.- POST /favorite/people/int:people_id
# 9.- DELETE /favorite/planet/int:planet_id
# 10.- DELETE /favorite/people/int:people_id

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

# Manejo de errores (APIException) como si fueran un JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Genera el sitemap con todos los endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#---------------------------------------

# RUTA 1.-
@app.route('/people', methods=['GET'])
def get_all_people():
    characters = Character.query.all()  # Obtiene todos los personajes
    return jsonify([char.serialize() for char in characters]), 200
#-----------------------------------------------------------------

# RUTA 2.-
@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    character = Character.query.get_or_404(people_id)  # Obtiene el personaje o manda 404 si no existe
    return jsonify(character.serialize()), 200
#------------------------------------------------

# RUTA 3.-
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()  # Obtiene todos los planetas
    return jsonify([planet.serialize() for planet in planets]), 200
#------------------------------------------------------------------

# RUTA 4.-
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)  # Obtiene el planeta o manda 404 si no existe
    return jsonify(planet.serialize()), 200

#-------------------------------------------
# RUTA 5.-
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()  # Obtiene todos los usuarios
    return jsonify([user.serialize() for user in users]), 200
#------------------------------------------------------------

# RUTA 6.-
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # Para este ejemplo, asumimos que el usuario con id = 1 está autenticado
    user_id = 1  # Esto debe cambiar cuando se implemente autenticación
    user = User.query.get_or_404(user_id)
    
    # Obtiene todos los favoritos del usuario
    favorites = [favorite.serialize() for favorite in user.favorites]
    return jsonify(favorites), 200
#--------------------------------------------------------------

# RUTA 7.-
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  # Esto debe cambiar cuando se implemente autenticación
    user = User.query.get_or_404(user_id)
    planet = Planet.query.get_or_404(planet_id)
    
    # Crea un nuevo favorito
    favorite = Favorite(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": f"El planeta {planet.name} ha sido agregado a tus favoritos."}), 201
#------------------------------------------------------------------------------

# RUTA 8.-
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user_id = 1  # Esto debe cambiar cuando se implemente autenticación
    user = User.query.get_or_404(user_id)
    character = Character.query.get_or_404(people_id)
    
    # Crea un nuevo favorito
    favorite = Favorite(user_id=user.id, character_id=character.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": f"¡El personaje {character.name} ha sido agregado a tus favoritos!"}), 201
#----------------------------------------------------------------------------------

# RUTA 9.-
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user_id = 1  # Esto debe cambiar cuando se implemente autenticación
    user = User.query.get_or_404(user_id)
    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Planeta eliminado de tus favoritos."}), 200
    return jsonify({"msg": "Este favorito no lo encontré."}), 404
#---------------------------------------------------------------------

# RUTA 10.-
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_person(people_id):
    user_id = 1  # Esto debe cambiar cuando se implemente autenticación
    user = User.query.get_or_404(user_id)
    favorite = Favorite.query.filter_by(user_id=user.id, character_id=people_id).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Personaje eliminado de tus favoritos."}), 200
    return jsonify({"msg": "Este favorito no lo encontré."}), 404

#---------------------------------------
# Este código solo corre si ejecutas `$ python src/app.py`
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
