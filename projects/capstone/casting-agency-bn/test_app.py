import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CastingAgencyCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Test actor',
            'age': 35,
            'gender': 'female',
        }

        self.new_movie = {
            'title': 'Test movie',
            'release_date': '2020-07-21T21:30:00.000Z',
        }

        self.assistant_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3ODE2YmZjY2EzMDAxOTdkNTVlMyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2NDk0MzYsImV4cCI6MTU5MTczNTgzNiwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.yctWKSC4m2lBJKioR4BWBdOWicUxU6wZZD8dGIj99pJkgeYLJ9cyP6-mgojKByJZ1N6vY7wR77kZu76_RmV0DTVytnkfBt4XsS7FvTwXGq520649cQfTN_If0fzm0nTwO428TvtpUFWzT90XYfLszOzbHcLw86iNMR3vwrWXg72aIKb9PEt3VKW8engSadVnwvH0oysJsOZLZ-gQbLJV2wqE05nYFWhECk_zQ72fIFJ1KVqzJBL82aemjLiXjyj2joPCTHXfQ5CmA8O0mn9bJlAS8DCUYZXnxL48ToajKnnfq4tdw0eOA5bRZlPZQ9dFfAMxBKbnNVRUyWfnsyIX-w'
        }

        self.director_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3OGI5MjI5ZGNlMDAxM2Q3OGVlZSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2NDk1MjEsImV4cCI6MTU5MTczNTkyMSwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZ3MiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDpjYXN0aW5ncyJdfQ.ADkAbby5iFnm13A9WaCWrLgtAN8K-yAydxrajkGqZX6HuIjgQWwFutVdwUxIgDRCblxnTY0kSONPiv1mumjVlKRVHTOOJzdFcBBYlvUt-XsXhpvbZQWgUxwfB6RGIexJnoiz_NOi9ftGRNmeiBF-LZ1YTOo_WViO-o4X_tzMdp8K_DmMeqPvyzbrc3dVr-E0w3AmXILJQqu2_akgj0feR51EzUCRy9XsQteltkSfQlZrCtQg1NYjwXCpIqzbm8rvbVXnLc95K_Vo4rJBNXVqjBukBQMckWw3wTEOz4Uff-pjnVegUq1BixzomPSAVv0mmTSEPxwWPnhBPbELUu6P8Q'
        }

        self.producer_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3OGRlYmZjY2EzMDAxOTdkNTY3ZiIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2NDk2MTYsImV4cCI6MTU5MTczNjAxNiwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZ3MiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6Y2FzdGluZ3MiLCJwb3N0Om1vdmllcyJdfQ.tzp_ID_YyJAw5T9vF7T9CLirvZ5YO_EHLBZmTMabl_3_ryo71gjnCVInNdo7kstN57NT5Xt8F7OLJl3Ad2w4UzC1IJLOJqxy9PhTMOhm8TDfSaOky91Q-2UHuv-xXDrqccU9rsiXF0CeFu0BhXfTt634HCtdoszLlNSwk3aGEWwDeo2I1Lyu9nuNg6MzTAYnOfA_KGjsySoeNcBFh4IFUtbMLUBoS6PoYSxiPzDy3OqvN_N4C074um83IuR8RuBsM9vJ0KpwmVmNGuhXo3fw8A7Mpezop7K5tPtHstZx1GUcNLzLUA834VYAO8JVd58vNEvP_xnWtAfR9X61UAvn8Q'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # ACTOR TESTS

    def test_get_actors(self):
        """Test retrieving all actors"""
        res = self.client().get('/actors', headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_no_auth(self):
        """Test retrieving all actors with no auth"""
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_actor(self):
        """Test retrieving specific actor"""
        res = self.client().get('/actors/10', headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['id'], 10)

    def test_404_non_existent_actor(self):
        """Test retrieving non-existing actor"""
        res = self.client().get('/actors/100', headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_new_actor_director(self):
        """Test adding a new actor with Director JWT"""
        res = self.client().post('/actors', json=self.new_actor, headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_add_new_actor_producer(self):
        """Test adding a new actor with Producer JWT"""
        res = self.client().post('/actors', json=self.new_actor, headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_add_new_actor_assistant(self):
        """Test adding a new actor with Assistant JWT"""
        res = self.client().post('/actors', json=self.new_actor, headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_405_if_actor_creation_not_allowed(self):
        """Test adding an actor with wrong endpoint"""
        res = self.client().post('/actors/100', json=self.new_actor)
        self.assertEqual(res.status_code, 405)

    def test_edit_actor_director(self):
        """Test modifying an actor with Director JWT"""
        res = self.client().patch('/actors/7', json=self.new_actor, headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 7)
        self.assertEqual(data['actor']['name'], self.new_actor['name'])

    def test_edit_actor_producer(self):
        """Test modifying an actor with Producer JWT"""
        res = self.client().patch('/actors/8', json=self.new_actor, headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 8)
        self.assertEqual(data['actor']['name'], self.new_actor['name'])

    def test_edit_actor_assistant(self):
        """Test modifying an actor with Assistant JWT"""
        res = self.client().patch('/actors/9', json=self.new_actor, headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_delete_actor_producer(self):
        """Test deleting an actor with producer token"""
        res = self.client().delete('/actors/1', headers=self.producer_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '1')
        self.assertEqual(actor, None)

    def test_delete_actor_director(self):
        """Test deleting an actor with director token"""
        res = self.client().delete('/actors/2', headers=self.director_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '2')
        self.assertEqual(actor, None)

    def test_delete_actor_assistant(self):
        """Test deleting an actor with assistant token"""
        res = self.client().delete('/actors/3', headers=self.assistant_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 3).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(actor)

    # MOVIE TESTS

    def test_get_movies(self):
        """Test retrieving all movies"""
        res = self.client().get('/movies', headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_movies_no_auth(self):
        """Test retrieving all movies with no auth"""
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_movie(self):
        """Test retrieving specific movie"""
        res = self.client().get('/movies/10', headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['id'], 10)

    def test_404_non_existent_movie(self):
        """Test retrieving non-existing movie"""
        res = self.client().get('/movies/100', headers=self.assistant_header)
        self.assertEqual(res.status_code, 404)

    def test_add_new_movie_director(self):
        """Test adding a new movie with Director JWT"""
        res = self.client().post('/movies', json=self.new_movie, headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_add_new_movie_producer(self):
        """Test adding a new movie with Producer JWT"""
        res = self.client().post('/movies', json=self.new_movie, headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_add_new_movie_assistant(self):
        """Test adding a new movie with Assistant JWT"""
        res = self.client().post('/movies', json=self.new_movie, headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_405_if_movie_creation_not_allowed(self):
        """Test adding a movie with wrong endpoint"""
        res = self.client().post('/movies/100', json=self.new_actor)
        self.assertEqual(res.status_code, 405)

    def test_edit_movie_director(self):
        """Test modifying a movie with Director JWT"""
        res = self.client().patch('/movies/7', json=self.new_movie, headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 7)
        self.assertEqual(data['movie']['title'], self.new_movie['title'])

    def test_edit_movie_producer(self):
        """Test modifying a movie with Producer JWT"""
        res = self.client().patch('/movies/8', json=self.new_movie, headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 8)
        self.assertEqual(data['movie']['title'], self.new_movie['title'])

    def test_edit_movie_assistant(self):
        """Test modifying a movie with Assistant JWT"""
        res = self.client().patch('/movies/9', json=self.new_movie, headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie_director(self):
        """Test deleting a movie with director token"""
        res = self.client().delete('/movies/1', headers=self.director_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(movie)

    def test_delete_movie_producer(self):
        """Test deleting a movie with producer token"""
        res = self.client().delete('/movies/2', headers=self.producer_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '2')
        self.assertEqual(movie, None)

    def test_delete_movie_assistant(self):
        """Test deleting a movie with assistant token"""
        res = self.client().delete('/movies/3', headers=self.assistant_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 3).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(movie)

    def test_add_new_movie_casting_director(self):
        """Test adding an actor casting to movie with Director JWT"""
        res = self.client().post('/movies/4/actors', json={'actor_id': 4}, headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 4)

    def test_add_new_movie_casting_producer(self):
        """Test adding an actor casting to movie with Producer JWT"""
        res = self.client().post('/movies/5/actors', json={'actor_id': 6}, headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 5)

    def test_add_new_movie_casting_assistant(self):
        """Test adding an actor casting to movie with Assistant JWT"""
        res = self.client().post('/movies/6/actors', json={'actor_id': 5}, headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_404_non_existent_actor_for_casting(self):
        """Test retrieving non-existing actor for casting"""
        res = self.client().post('/movies/7/actors', json={'actor_id': 11}, headers=self.producer_header)
        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

