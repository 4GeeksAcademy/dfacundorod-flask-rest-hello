from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    Favorite_character = db.relationship('Favorite_character', backref='user', lazy=True)
    Favorite_planet = db.relationship('Favorite_planet', backref='user', lazy=True)
   
    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "lastname": self.lastname
        }
    

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    climate=db.Column(db.String, nullable=False)
    population= db.Column(db.Integer, nullable=False)
    terrain=db.Column(db.String, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "climate": self.climate,
            "name": self.name,
            "population": self.population,
            "terraion": self.terrain
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    gender= db.Column(db.String, nullable=False)
    hair_color= db.Column(db.String, nullable=False)
    eye_color=db.Column(db.String, nullable=False)
    age=db.Column(db.Integer, nullable=False)
    planet= db.Column(db.String, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "name": self.name,
            "age": self.age,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color
        }




class Favorite_character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    def __repr__(self):
        return '<Favorite %r>' %self.user_id
    
    def serialize(self):
        return {
        'id': self.id,
        'user_id': self.user_id,
        'character_id' : self.character_id
        }

class Favorite_planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    def __repr__(self):
        return '<Favorite %r>' %self.user_id
    
    def serialize(self):
        return {
        'id': self.id,
        'user_id': self.user_id,
        'planet_id' : self.planet_id
        }

    
