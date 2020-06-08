import os
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "castingagency"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# Aux function for changing boolean gender to female/male
# for easier understanding in client perspective


def gender_string(gender):
    if gender:
        return 'female'
    else:
        return 'male'


'''
Castings - association table allowing
Many-to-Many relationship between movies and actors

'''


castings = db.Table('castings',
                    db.Column('actor_id',
                              db.Integer,
                              db.ForeignKey('actor.id'),
                              primary_key=True),
                    db.Column('movie_id',
                              db.Integer,
                              db.ForeignKey('movie.id'),
                              primary_key=True)
                    )


'''
Movie

'''


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    actors = db.relationship('Actor', secondary=castings,
                             backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'num_actors_casted': len(self.actors),
            'actors_casted': [{
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
                'gender': gender_string(actor.gender),
            }
                for actor in self.actors
            ],
        }


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
    # Simplifying gender to binary choice. female = true, male = false

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': gender_string(self.gender),
            'num_movie_castings': len(self.movies),
            'movie_castings': [{
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date,
            }
                for movie in self.movies
            ],
        }
