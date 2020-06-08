import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
import json

from models import setup_db, Movie, Actor

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # ACTOR ENDPOINTS

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors/<actor_id>')
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format()
            })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = int(body.get('age', None))
        new_gender = body.get('gender', None)

        boolean_gender = new_gender == 'female'

        try:
            actor = Actor(name=new_name, age=new_age, gender=boolean_gender)
            actor.insert()

            actors = Actor.query.order_by(Actor.id).all()

            return jsonify({
                'success': True,
                'actors': [act.format() for act in actors]
            })
        except BaseException:
            abort(422)

    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, actor_id):
        body = request.get_json()

        name = body.get('name', None)
        age = int(body.get('age', None))
        gender = body.get('gender', None)

        boolean_gender = gender == 'female'

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)
        else:
            try:
                actor.name = name
                actor.age = age
                actor.gender = boolean_gender
                actor.update()

                updated_actor = Actor.query\
                    .filter(Actor.id == actor_id)\
                    .one_or_none()

                return jsonify({
                    'success': True,
                    'actor': updated_actor.format(),
                })
            except BaseException:
                abort(422)

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        else:
            try:
                actor.delete()

                return jsonify({
                    'success': True,
                    'delete': actor_id
                })
            except BaseException:
                abort(422)

    # MOVIE ENDPOINTS

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/movies/<movie_id>')
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movie': movie.format(),
            })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            movies = Movie.query.order_by(Movie.id).all()

            return jsonify({
                'success': True,
                'movies': [mov.format() for mov in movies],
            })
        except BaseException:
            abort(422)

    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(payload, movie_id):
        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)
        else:
            try:
                movie.title = title
                movie.release_date = release_date
                movie.update()

                updated_movie = Movie.query\
                    .filter(Movie.id == movie_id)\
                    .one_or_none()

                return jsonify({
                    'success': True,
                    'movie': updated_movie.format(),
                })
            except BaseException:
                abort(422)

    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            try:
                movie.delete()

                return jsonify({
                    'success': True,
                    'delete': movie_id
                })
            except BaseException:
                abort(422)

    @app.route('/movies/<movie_id>/actors', methods=['POST'])
    @requires_auth('post:castings')
    def create_casting(payload, movie_id):
        body = request.get_json()

        actor_id = body.get('actor_id', None)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if movie is None or actor is None:
            abort(404)
        else:
            try:
                movie.actors.append(actor)
                actor.movies.append(movie)
                movie.update()
                actor.update()

                movie_cast = Movie.query\
                    .filter(Movie.id == movie_id)\
                    .one_or_none()

                return jsonify({
                    'success': True,
                    'movie': movie_cast.format(),
                })
            except BaseException:
                abort(422)

    @app.route('/movies/<movie_id>/actors', methods=['DELETE'])
    @requires_auth('delete:castings')
    def delete_casting(payload, movie_id):
        body = request.get_json()

        actor_id = body.get('actor_id', None)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if movie is None or actor is None:
            abort(404)
        else:
            try:
                movie.actors.remove(actor)
                movie.update()

                movie_cast = Movie.query \
                    .filter(Movie.id == movie_id) \
                    .one_or_none()

                return jsonify({
                    'success': True,
                    'movie': movie_cast.format(),
                })
            except BaseException:
                abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422


    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(500)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500


    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            'success': False,
            'error': e.status_code,
            'message': e.error['description']
        }), e.status_code

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)