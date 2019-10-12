import os
from flask import Flask, request, abort, jsonify, render_template, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_questions(request, selection):
  page = request.args.get('page',1,type=int)
  start =(page-1)*QUESTIONS_PER_PAGE
  end =start + QUESTIONS_PER_PAGE

  questions = [quetion.format() for question in selection]
  current_question = questions[start:end]

  return current_question

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  #@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs --> DONE
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  setup_db(app)
  
  #@TODO: Use the after_request decorator to set Access-Control-Allow --> DONE
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  #@TODO: Create an endpoint to handle GET requests for all available categories.
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = db.session.query(categories.type).all()
    return categories

  #@TODO: Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
  #TEST: At this point, when you start the applicationyou should see questions and categories generated, ten questions per page and pagination at the bottom of the screen for three pages. Clicking on the page numbers should update the questions.
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions(id):
    request = db.session.query(categories).join(questions).filter(categories.id == id).all()
    current_questions = paginate_questions(request,selection)
    if len(current_questions) ==0:
      abort(404)

    return jsonify({
      'success': True,
      'questions':current_questions,
      'total_questions': len(questions.query.all())
    })
  
  #@TODO: Create an endpoint to DELETE question using a question ID.
  #TEST: When you click the trash icon next to a question, the question will be removed. This removal will persist in the database and when you refresh the page.
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = db.session.query(questions).filter_by(id=id).first()
      db.session.delete(question)
      db.session.commit()
      #flash('Question with ID: '+id+' has been successfully deleted')
    except:
      #flash('An error occurred and question with ID: '+id+' could not be deleted deleted')
      db.session.rollback()
    finally:
      db.session.close()

  #@TODO:Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
  #TEST: When you submit a question on the "Add" tab, the form will clear and the question will appear at the end of the last page of the questions list in the "List" tab.
  @app.route('/questions', methods=['POST'])
  def create_question():
    question = request.form.get('question')
    answer = request.form.get('answer')
    difficulty = request.form.get('difficulty')
    category = request.form.get('category')
    try:
      question = questions(question=question,answer=answer,difficulty=difficulty,category=category)
      db.session.add(question)
      db.session.commit()
      #flash('question: '+request.form.get('question')+'. was successfully saved')
    except:
      #flash('An error occured, and question: '+request.form.get('question')+'. could not be saved')
      db.session.rollback()
    finally:
      db.session.close()

  #@TODO: Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
  #TEST: Search by any phrase. The questions list will update to include only question that include that string within their question. Try using the word "title" to start.
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    #Initialize variables
    results = {}
    data = []
    search_term = request.form.get('input')
    search = "%{}%".format(search_term)
    search_results = db.session.query(questions.question, questions.category).filter(
        questions.question.like(search)).all()
    for search_result in search_results:
      results["question"] = search_result[0]
      results["category"] = search_result[1]
      data.append(results)
  #return results=data

  #@TODO: Create a GET endpoint to get questions based on category. 
  #TEST: In the "List" tab / main screen, clicking on one of the categories in the left column will cause only questions of that category to be shown. 
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def category_questions(id):
    total_questions = db.session.query(func.count(questions.question).join(categories).filter(categories.id==id).first()
    questions = db.session.query(questions.question,questions.category).join(categories).filter(categories.id==id).all()
  #to continue what to return

  #@TODO: Create error handlers for all expected errors including 404 and 422. 
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

  return app


'''
#@TODO: Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category,if provided, and that is not one of the previous questions. 
#TEST: In the "Play" tab, after a user selects "All" or a category,one question at a time is displayed, the user is allowed to answer and shown whether they were correct or not. 



'''

'''

 
'''
    
