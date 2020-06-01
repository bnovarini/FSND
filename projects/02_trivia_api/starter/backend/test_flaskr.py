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
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Is this a test question?',
            'answer': 'Yes it is',
            'difficulty': 5,
            'category': 2
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

    def test_get_categories(self):
        """Test retrieving all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_get_paginated_questions(self):
        """Test retrieving paginated questions"""
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["current_category"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        """Test if receive 404 when requesting beyond valid page"""
        res = self.client().get('/questions?page=1000000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], 'resource not found')

    def test_delete_question(self):
        """Test deleting a question"""
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["current_category"]))
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        """Test deleting a question that doesn't exist"""
        res = self.client().delete('/questions/100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_create_new_question(self):
        """Test creating a new question"""
        questions_before = Question.query.count()
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["total_questions"], questions_before + 1)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["current_category"]))

    def test_405_if_question_creation_not_allowed(self):
        """Test creating a new question with wrong endpoint"""
        res = self.client().post('/questions/100', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_question_search_with_results(self):
        """Test getting questions from search results"""
        res = self.client().post('/questions', json={'searchTerm': 'Anne'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data["total_questions"], 1)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))
        self.assertEqual(data["current_category"], [4])

    def test_get_question_search_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'dhsjd'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["current_category"]))

    def test_get_paginated_questions_in_category(self):
        """Test retrieving paginated questions inside a category"""
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['total_questions'], 3)
        self.assertEqual(len(data['questions']), 3)
        self.assertTrue(len(data["categories"]))
        self.assertEqual(data["current_category"], [0])

    def test_get_next_quiz_question_category(self):
        """Test getting next random question for specific category in quiz"""
        res = self.client().post(
            '/quizzes',
            json={
                'quiz_category': {
                    'type': 'Science',
                    'id': 0},
                'previous_questions': [22, 21]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertNotEqual(data['question']['id'], 22)
        self.assertNotEqual(data['question']['id'], 21)

    def test_get_next_quiz_question_all_categories(self):
        """Test retrieving next random question for all categories in quiz"""
        question_ids_expect_9 = [
            5,
            2,
            4,
            6,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24]
        res = self.client().post('/quizzes', json={'quiz_category': {
            'type': 'click',
            'id': 0},
            'previous_questions':
            question_ids_expect_9})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['question']['id'], 9)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
