import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.order_by(Drink.id).all()

    if len(drinks) == 0:
        abort(404)

    return jsonify(
        {'success': True,
         'drinks': [
             drink.short() for drink in drinks]
         })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.order_by(Drink.id).all()

    if len(drinks) == 0:
        abort(404)

    return jsonify(
        {'success': True,
         'drinks': [
             drink.long() for drink in drinks]
         })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_new_drink(payload):
    body = request.get_json()

    title = body.get('title', None)
    recipe = json.dumps(body.get('recipe', None))

    try:
        drink = Drink(
            title=title,
            recipe=recipe)
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except BaseException:
        abort(422)


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload, drink_id):
    body = request.get_json()

    title = body.get('title', None)
    recipe = json.dumps(body.get('recipe', None))

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
    else:
        try:
            drink.title = title
            drink.recipe = recipe
            drink.update()

            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            })
        except BaseException:
            abort(422)


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
    else:
        try:
            drink.delete()

            return jsonify({
                'success': True,
                'delete': drink_id
            })
        except BaseException:
            abort(422)


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify({
      "success": False,
      "error": e.status_code,
      "message": e.error['description']
    }), e.status_code
