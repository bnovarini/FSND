import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# Using similar pagination implementation as code for bookshelf api in
# Udacity course
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)

        return jsonify({'success': True, 'categories': [
                       category.format()['type'] for category in categories]})

    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_category = [
            category.format()["category"]
            for category in Question.query.order_by(
                Question.category).distinct(
                Question.category)]
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()

        return jsonify({
            "success": True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': current_category,
            'categories': [category.format()['type']
                           for category in categories]
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            current_category = [
                category.format()["category"]
                for category in Question.query.order_by(
                    Question.category).distinct(
                    Question.category)]
            categories = Category.query.order_by(Category.id).all()

            return jsonify({
                "success": True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': current_category,
                'categories': [category.format()['type']
                               for category in categories]
            })

        except BaseException:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search_term = body.get('searchTerm', None)

        try:
            if search_term:
                questions = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).order_by(
                    Question.id).all()

                current_questions = paginate_questions(request, questions)
                current_category = [
                    category.format()["category"]
                    for category in Question.query.order_by(
                        Question.category).distinct(
                        Question.category)]
                categories = Category.query.order_by(Category.id).all()

                return jsonify({
                    "success": True,
                    'questions': current_questions,
                    # assuming in this case we care about total questions for
                    # that search
                    'total_questions': len(questions),
                    'current_category': current_category,
                    'categories': [category.format()['type']
                                   for category in categories]
                })

            else:
                cat_id = str(int(new_category) + 1)
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=cat_id,
                    difficulty=new_difficulty)
                question.insert()

                questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)
                current_category = [
                    category.format()["category"]
                    for category in Question.query.order_by(
                        Question.category).distinct(
                        Question.category)]
                categories = Category.query.order_by(Category.id).all()

                return jsonify({
                    "success": True,
                    'questions': current_questions,
                    'total_questions': len(questions),
                    'current_category': current_category,
                    'categories': [category.format()['type']
                                   for category in categories]
                })

        except BaseException:
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def retrieve_questions_in_category(category_id):
        cat_id = category_id + 1
        questions = Question.query.filter(
            Question.category == cat_id
        ).order_by(
            Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.id).all()

        return jsonify({
            "success": True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': [category_id],
            'categories': [category.format()['type']
                           for category in categories]
        })

    @app.route('/quizzes', methods=['POST'])
    def get_questions_for_quiz():
        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        category_id = int(body.get('quiz_category', None)["id"])
        category_type = body.get('quiz_category', None)["type"]
        cat_id = category_id + 1

        if category_type == 'click':
            category_questions = Question.query.order_by(func.random())
        else:
            category_questions = Question.query.filter(
                Question.category == cat_id
            ).order_by(
                func.random())

        previous_question_ids = [q for q in previous_questions]

        next_question = category_questions.filter(
            Question.id.notin_(previous_question_ids)).first()

        if next_question is None:
            return jsonify({
                "success": True,
                'question': None
            })
        else:
            return jsonify({
                "success": True,
                'question': next_question.format()
            })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
