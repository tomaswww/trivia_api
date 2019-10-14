import os
from flask import Flask, request, abort, jsonify, render_template, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_questions(request, questions):
  page = request.args.get('page',1,type=int)
  start =(page-1)*QUESTIONS_PER_PAGE
  end =start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in questions]
  current_question = questions[start:end]

  return current_question

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  #@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs --> DONE
  CORS(app)
  
  
  #@TODO: Use the after_request decorator to set Access-Control-Allow --> DONE
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  #@TODO: Create an endpoint to handle GET requests for all available categories. --> DONE
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    fixed_categories = [category.format() for category in categories]
    return jsonify({
      'success':True,
      'categories':fixed_categories,
      'total_categories':len(fixed_categories)
    })

  #@TODO: Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.--> DONE
  #TEST: At this point, when you start the application you should see questions and categories generated, ten questions per page and pagination at the bottom of the screen for three pages. Clicking on the page numbers should update the questions.
  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.all()
    categories = Category.query.all()

    fixed_questions = paginate_questions(request,questions)
    fixed_categories = [category.format() for category in categories]

    if len(fixed_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions':fixed_questions,
      'total_questions': len(questions),
      'categories': fixed_categories,
      'current_category': list(set([fixed_question['category']for fixed_question in fixed_questions]))
    })
  
  #@TODO: Create an endpoint to DELETE question using a question ID. --> DONE
  #TEST: When you click the trash icon next to a question, the question will be removed. This removal will persist in the database and when you refresh the page.
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.filter_by(Question.id==id).one_or_none()

      if question is None:
        abort(404)
      else:
        question.delete()
        current_questions = Question.query.all()
        new_total = len(current_questions)
        return jsonify({
          'success':True,
          'deleted':id,
          'total_questions':new_total
        })
    except:
      abort(422)

  #@TODO:Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.--> DONE
  #TEST: When you submit a question on the "Add" tab, the form will clear and the question will appear at the end of the last page of the questions list in the "List" tab.
  @app.route('/questions', methods=['POST'])
  def create_question():
    question = request.form.get('question')
    answer = request.form.get('answer')
    difficulty = request.form.get('difficulty')
    category = request.form.get('category')
    try:
      question = Question(question=question,answer=answer,difficulty=difficulty,category=category)
      question.insert()
      current_questions = Question.query.all()
      new_total = len(current_questions)
      return jsonify({
        'success':True,
        'total_questions':new_total,
        'created':question.id
      })
    except:
      abort(422)

  #@TODO: Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. --> DONE
  #TEST: Search by any phrase. The questions list will update to include only question that include that string within their question. Try using the word "title" to start.
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    try:
      search_term = request.form.get('input')
      search = "%{}%".format(search_term)
      search_results = Question.query.filter(Question.question.like(search)).all()
      fixed_results = paginate_questions(request,search_results)

      if len(search_results)==0:
        abort(404)
      
      return jsonify({
        'success':True,
        'questions': fixed_results,
        'total_questions':len(search_results)
      })
    except:
      abort(422)

  #@TODO: Create a GET endpoint to get questions based on category. --> DONE
  #TEST: In the "List" tab / main screen, clicking on one of the categories in the left column will cause only questions of that category to be shown. 
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def category_questions(id):
    try:
      questions = Question.query.join(Category).filter(Category.id==id).all()
      categories = Category.query(Category.type).filter(Category.id==id).first()
      fixed_questions = paginate_questions(request,questions)
      fixed_category = [category.format() for category in categories]

      if len(questions) ==0:
        abort(404)

      return jsonify({
        'success':True,
        'questions':fixed_questions,
        'total_questions':len(questions),
        'current_category': fixed_category
      })
    except:
      abort(422)
   

  #@TODO: Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category,if provided, and that is not one of the previous questions. --> DONE
  #TEST: In the "Play" tab, after a user selects "All" or a category,one question at a time is displayed, the user is allowed to answer and shown whether they were correct or not. 
  @app.route('/quizzes', methods=['POST'])
  def play():
    #DATA returned from the FE
    data = request.get_json()
    previous_questions = data['previous_questions']
    quiz_category = data['quiz_category']
    
    #Logic here
    #1.Check if user provided category
    if quiz_category['id']:
      questions = Question.query.join(Category.id).filter(Category.id==quiz_category['id']).all()
    else:
      questions = Question.query.all()
    fixed_questions = [question.format() for question in questions]
    #2.Check if that question has been used before
    questions_available =[]
    for fixed_question in fixed_questions:
      if fixed_question['id'] not in previous_questions:
        questions_available.append(fixed_question)
    #3.Random select a question from available
    random_question = None
    if len(questions_available)==0:
      abort(404)
    else:
      random_question = random.choice(questions_available)
    return jsonify({
      'success': True,
      'question': random_question
    })


  #@TODO: Create error handlers for all expected errors including 404 and 422. --> DONE
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False, 
          "error": 404,
          "message": "Not found"
          }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable Entity"
          }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method not allowed"
          }), 405

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request error"
      }), 400


  @app.errorhandler(500)
  def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500 

  return app




    
