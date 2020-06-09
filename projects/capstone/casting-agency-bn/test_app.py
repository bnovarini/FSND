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
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3ODE2YmZjY2EzMDAxOTdkNTVlMyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2NjAzOTEsImV4cCI6MTU5MTc0Njc5MSwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Qhrp7IBiNZOY2X5KFOZA-TWcv_VBTYxH6AmiS47LwcyTZj9GvMvMma3ocF4lM8Y6Qm2DRiof5H_z89NKeURdnH0MF8HHjmrz6Z4azTFm4Fo-pkMnsKxhcnoN3FhA-GWZOdlMl3IeuM6c2fHd1VOf3u5Gt5xXSFtkMmxXCnP9-6oV__6VzWrfSIDo_H6k66nvvNGV59wfpOiE3RTBFqDtjl9082sua8hM4YDzJ6nynV0Pt6LqXU7O6QsymJ2aTDaLxoOl9J9YxFjVHeC9dHe-HmgnbWXN9t_3HhLy7BbOMuna9Qu7AtD0_z3qX5aNKFz_MBNIG0DuU30zfH8whalRMg'
        }

        self.director_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3OGI5MjI5ZGNlMDAxM2Q3OGVlZSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2NjA0MzAsImV4cCI6MTU5MTc0NjgzMCwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZ3MiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDpjYXN0aW5ncyJdfQ.E499AgccW1pXYWiPBalfnRWuBxWseIL8Bl--UiN3_OaGMJ4BOU96mwMqcyYpZI4jRk7DokI8rTwC0gE-MCyO7fZv3luIUUxMyFqKM8UkeC2gakD1xo8gcsikqGQLFjMjnyEyO_CMFCoCMX76CbqmbASL404ZVz2M9mwJFwD6wVGdp_Ww3EtzJRY1XsjjpbXl3PuMLmt8waoZfPS4gpTNRVqhXAD779UXNqsImbFaktHtsvfsQ8sqyHVeeFb7iugro_nxddiaaLfLKWsP8n6vQeS1VO50oowJj0cwSyqq-DVc1qbUNjjTtaLWSflvvc6sec2VxvotvU-oCkgvEm-SUA'
        }

        self.producer_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3OGRlYmZjY2EzMDAxOTdkNTY3ZiIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2NjA0NjgsImV4cCI6MTU5MTc0Njg2OCwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZ3MiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6Y2FzdGluZ3MiLCJwb3N0Om1vdmllcyJdfQ.R8UxOHnNPGGPwsLyuuezzD5SaIjhYVG1FETt1qQ_WL3DB7IIz0yZpxGCqY18EsXwVEvwFuC4Shzgs67O1D7qKj0i5ivJo7OTzgRy3RTwCs7r9U-onYhw03ohBN3x2iyn43kXts0atF60_XbucER--rDbajqjvGAddPXMzqjm0xLX-F8hXgatibFperOqXwZiWU_Axnjj4xf-FHMKV3WvDpp2jHTbOL3YUoTrnGrShDwKVlnlJbJo3Tt1j-yqibdS7SXyE1qGre48Qt7hj849cPhoAfTItRFqZRFJrNmlsaG9CWLawG402ewySp0O4G43z9jcNfsXVihJDdqzyAhS9Q'
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
        res = self.client().get('/actors',
                                headers=self.assistant_header)
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
        res = self.client().get('/actors/10',
                                headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['id'], 10)

    def test_404_non_existent_actor(self):
        """Test retrieving non-existing actor"""
        res = self.client().get('/actors/100',
                                headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_new_actor_director(self):
        """Test adding a new actor with Director JWT"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_add_new_actor_producer(self):
        """Test adding a new actor with Producer JWT"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_add_new_actor_assistant(self):
        """Test adding a new actor with Assistant JWT"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_405_if_actor_creation_not_allowed(self):
        """Test adding an actor with wrong endpoint"""
        res = self.client().post('/actors/100',
                                 json=self.new_actor)
        self.assertEqual(res.status_code, 405)

    def test_edit_actor_director(self):
        """Test modifying an actor with Director JWT"""
        res = self.client().patch('/actors/7',
                                  json=self.new_actor,
                                  headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 7)
        self.assertEqual(data['actor']['name'], self.new_actor['name'])

    def test_edit_actor_producer(self):
        """Test modifying an actor with Producer JWT"""
        res = self.client().patch('/actors/8',
                                  json=self.new_actor,
                                  headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 8)
        self.assertEqual(data['actor']['name'], self.new_actor['name'])

    def test_edit_actor_assistant(self):
        """Test modifying an actor with Assistant JWT"""
        res = self.client().patch('/actors/9',
                                  json=self.new_actor,
                                  headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_delete_actor_producer(self):
        """Test deleting an actor with producer token"""
        res = self.client().delete('/actors/1',
                                   headers=self.producer_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '1')
        self.assertEqual(actor, None)

    def test_delete_actor_director(self):
        """Test deleting an actor with director token"""
        res = self.client().delete('/actors/2',
                                   headers=self.director_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '2')
        self.assertEqual(actor, None)

    def test_delete_actor_assistant(self):
        """Test deleting an actor with assistant token"""
        res = self.client().delete('/actors/3',
                                   headers=self.assistant_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 3).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(actor)

    # MOVIE TESTS

    def test_get_movies(self):
        """Test retrieving all movies"""
        res = self.client().get('/movies',
                                headers=self.assistant_header)
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
        res = self.client().get('/movies/10',
                                headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['id'], 10)

    def test_404_non_existent_movie(self):
        """Test retrieving non-existing movie"""
        res = self.client().get('/movies/100',
                                headers=self.assistant_header)
        self.assertEqual(res.status_code, 404)

    def test_add_new_movie_director(self):
        """Test adding a new movie with Director JWT"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_add_new_movie_producer(self):
        """Test adding a new movie with Producer JWT"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_add_new_movie_assistant(self):
        """Test adding a new movie with Assistant JWT"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_405_if_movie_creation_not_allowed(self):
        """Test adding a movie with wrong endpoint"""
        res = self.client().post('/movies/100',
                                 json=self.new_actor)
        self.assertEqual(res.status_code, 405)

    def test_edit_movie_director(self):
        """Test modifying a movie with Director JWT"""
        res = self.client().patch('/movies/7',
                                  json=self.new_movie,
                                  headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 7)
        self.assertEqual(data['movie']['title'], self.new_movie['title'])

    def test_edit_movie_producer(self):
        """Test modifying a movie with Producer JWT"""
        res = self.client().patch('/movies/8',
                                  json=self.new_movie,
                                  headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 8)
        self.assertEqual(data['movie']['title'], self.new_movie['title'])

    def test_edit_movie_assistant(self):
        """Test modifying a movie with Assistant JWT"""
        res = self.client().patch('/movies/9',
                                  json=self.new_movie,
                                  headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie_director(self):
        """Test deleting a movie with director token"""
        res = self.client().delete('/movies/1',
                                   headers=self.director_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(movie)

    def test_delete_movie_producer(self):
        """Test deleting a movie with producer token"""
        res = self.client().delete('/movies/2',
                                   headers=self.producer_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '2')
        self.assertEqual(movie, None)

    def test_delete_movie_assistant(self):
        """Test deleting a movie with assistant token"""
        res = self.client().delete('/movies/3',
                                   headers=self.assistant_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 3).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(movie)

    def test_add_new_movie_casting_director(self):
        """Test adding an actor casting to movie with Director JWT"""
        res = self.client().post('/movies/4/actors',
                                 json={'actor_id': 4},
                                 headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 4)

    def test_add_new_movie_casting_producer(self):
        """Test adding an actor casting to movie with Producer JWT"""
        res = self.client().post('/movies/5/actors',
                                 json={'actor_id': 6},
                                 headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 5)

    def test_add_new_movie_casting_assistant(self):
        """Test adding an actor casting to movie with Assistant JWT"""
        res = self.client().post('/movies/6/actors',
                                 json={'actor_id': 5},
                                 headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_404_non_existent_actor_for_casting(self):
        """Test retrieving non-existing actor for casting"""
        res = self.client().post('/movies/7/actors',
                                 json={'actor_id': 11},
                                 headers=self.producer_header)
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
