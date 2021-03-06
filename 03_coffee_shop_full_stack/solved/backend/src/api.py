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
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN

# db_drop_and_create_all()
'''
'''
## ROUTES

@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
returns status code 200 and json {"success": True, "drinks": drinks}
where drinks is the list of drinks
or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    formatted_drinks = []
    for d in drinks:
        record = d.short()
        formatted_drinks.append(record)
    return jsonify({
        'success': True,
        'drinks': formatted_drinks
        })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drink_details')
def get_drinks_details(payload):
    drinks = Drink.query.all()
    formatted_drinks = []
    for d in drinks:
        record = d.long()
        formatted_drinks.append(record)
    return jsonify({
        'success': True,
        'drinks': formatted_drinks
        })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drink')
def create_new_drink(payload):
    Message_body = request.get_json()
    New_drink = Drink()
    if not Message_body:
        abort(400)
    title = Message_body.get('title', None)
    recipe = Message_body.get('recipe', None)
    if not title or not recipe:
        abort(400)
    New_drink.title = title
    # Note: refrence used
    # for dupm function https://docs.python.org/3/library/json.html
    New_drink.recipe = recipe if type(recipe) == str else json.dumps(recipe)
    New_drink.insert()
    return jsonify({'success': True}), 201


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drink')
def update_drink(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    Message_body = request.get_json()
    drink.title = Message_body.get('title')
    drink.update()
    drinks = Drink.query.all()
    formatted_drinks = []
    for d in drinks:
        record = d.long()
        formatted_drinks.append(record)
    return jsonify({
        'success': True,
        'drinks': formatted_drinks
    })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drink')
def delete_drink(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    drink.delete()
    return jsonify({
        'success': True,
        'deleted': id
    })

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def resourceNotFound(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(401)
def notAuthorized(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "not authorized to access API"
                    }), 401


@app.errorhandler(403)
def notAuthorizedResource(error):
    return jsonify({
                    "success": False,
                    "error": 403,
                    "message": "you do not have access to this resource"
                    }), 403


@app.errorhandler(400)
def BadRequest(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "bad request, you did not provide information"
                    }), 400


@app.errorhandler(AuthError)
def handle_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code

