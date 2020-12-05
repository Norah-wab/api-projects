import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  db = SQLAlchemy(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resource={r'/api/*': {'origins': '*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request (response):
    response.headers.add('Access-Control-Allow-Headers','Contect-Type, Autherization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_question_categories():
    category = Category.query.all()
    formatted_category = {
                    c.id: c.type for c in category
                }
    return jsonify({
      'success': True,
      'category':formatted_category
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    try:
      page = request.args.get('page',1,type=int)
      start = (page - 1) * 10
      end = start + 10
      questions = Question.query.all()
      formatted_questions = [q.format() for q in questions]
      categories = Category.query.all()
      formated_category = [c.format() for c in categories]
      questions_paginated = formatted_questions[start:end]
      if len(questions_paginated) == 0:
        abort(404)
      return jsonify({
        'success' : True,
        'questions':questions_paginated,
        'totalQuestions':len (formatted_questions),
        'categories' : formated_category ,
        'current_category': None})
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_specific_question(question_id):
    try:
      Question.query.get(question_id).delete()
      return jsonify({
        'success': True,
        'deleted': question_id
      })
    except:
      abort(404)
    
  '''
  @TODO:  
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',methods=['POST'])
  def create_New_question():
    Message_body = request.get_json()
    search = Message_body.get('searchTerm', None)
    if search is not None:
      result = Question.query.filter(Question.question.ilike(f'%{search}%'))
      current_questions = [q.format() for q in result]
      if len(current_questions) == 0:
        abort(404)
      else:
        return jsonify({
                    'success': True,
                    'search_term': search,
                    'questions': current_questions,
                    'total_matching_questions': len(current_questions),
                    'total_questions': len(Question.query.all())
                })
    else:
      Newquestion = Message_body.get('question',None)
      NewAnswer = Message_body.get('answer',None)
      NewCategory = Message_body.get('category',None)
      NewDifficulty = Message_body.get('difficulty',None)
      if ((Newquestion is None) or (NewAnswer is None) or (NewDifficulty is None) or (NewCategory is None)):
        abort(422)
      try:
        question = Question(question = Newquestion,answer = NewAnswer,category = NewCategory,difficulty = NewDifficulty)
        question.insert()
        return jsonify({'success' : True})
      except:
        abort(400)
  '''
  @TODO:  
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_question_based_on_category(category_id):
    try:
      category = Category.query.get(category_id)
      questions_category = Question.query.filter(Question.category == category.id).all()
      if ((category is None) or (questions_category is None)):
        abort(422)
      else:
        formatted_questions = [q.format() for q in questions_category]
        return jsonify({
        'success' : True,
        'questions':formatted_questions,
        'total_questions': len(Question.query.all()),
        'total_in_category': len(formatted_questions),
        'current_category': category.format()
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def quiz():
    try:
      body = request.get_json()
      quiz_category = body.get('quiz_category',None)
      previous_questions = body.get('previous_questions')
    
      previous_questions_id  = [ pq for pq in previous_questions]
      questions = Question.query.filter(Question.category == quiz_category['id']).filter(Question.id.notin_(previous_questions_id))
      formatted_questions = [q.format() for q in questions]
      nextQuestion = random.choice(formatted_questions)
      return jsonify(
                { 'success': True, 
                  'questions': nextQuestion
                })
    except:
      abort(422)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def Error_404(error):
    return jsonify({
        "error": 404,
        "message": "page not found or requested data not found",
        "success": False
        }), 404
  @app.errorhandler(422)
  def Error_422(error):
    return jsonify({
        "error": 422,
        "message": "can not processed please check later",
        "success": False
        }), 422
  @app.errorhandler(405)
  def Error_405(error):
    return jsonify({
        "error": 405,
        "message": "this method not allowed, maybe wrong method requested",
        "success": False
        }), 405
  @app.errorhandler(400)
  def Error_400(error):
    return jsonify({
        "error": 400,
        "message": "this is bad request, somthing went wrong",
        "success": False
        }), 400
  return app
