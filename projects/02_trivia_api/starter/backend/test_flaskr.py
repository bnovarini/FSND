import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # self.new_book = {
        #     'title': 'Anansi Boys',
        #     'author': 'Neil Gaiman',
        #     'rating': 5
        # }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        """Test retrieving all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["categories"]))

    def test_get_paginated_questions(self):
        """Test retrieving paginated questions"""
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        """Test if receive 404 when requesting beyond valid page"""
        res = self.client().get('/questions?page=1000000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue(data["message"],'resource not found')

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()