from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Tabla User
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favorites": [favorite.serialize() for favorite in self.favorites]  # Incluye los favoritos
        }

    def __repr__(self):
        return f'<User {self.username}>'

# Tabla Character
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    birth_year = db.Column(db.String(20), nullable=True)
    favorites = db.relationship('Favorite', backref='character', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "favorites_count": len(self.favorites)  # Cantidad de favoritos asociados
        }

    def __repr__(self):
        return f'<Character {self.name}>'

# Tabla Planet
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    climate = db.Column(db.String(50), nullable=True)
    terrain = db.Column(db.String(50), nullable=True)
    population = db.Column(db.String(50), nullable=True)
    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "favorites_count": len(self.favorites)  # Cantidad de favoritos asociados
        }

    def __repr__(self):
        return f'<Planet {self.name}>'

# Tabla Favorite
class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.serialize() if self.character else None,  # Serializa el personaje si existe
            "planet": self.planet.serialize() if self.planet else None  # Serializa el planeta si existe
        }

    def __repr__(self):
        return f'<Favorite User: {self.user_id}, Character: {self.character_id}, Planet: {self.planet_id}>'
