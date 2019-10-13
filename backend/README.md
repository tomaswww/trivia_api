# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Avaible Endpoints

In order to play the game, a number of operations take place, each one of them belong to a specific endpoint. The available operations are:

- [GET categories](#getCategories)
- [GET questions](#getQuestions1)
- [GET questions (for a specific category)](#getQuestions2)
- [DELETE question](#deleteQuestion)
- [POST question (create question)](#createQuestion)
- [POST question (search question)](#postQuestion)
- [POST quizzes (to play game)](#postQuizzes)

***
<h4 id="getCategories"></h4>

> **GET '/categories'**

This endpoint fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

**Request Arguments:** 
- *None*

**Returns:** The return should include an success: True message along with the total categories (amount).
Also should include an object with a single key, categories, that contains a object of id: category_string key:value pairs, something like this:

```javascript
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```
***
<h4 id="getQuestions1"></h4>

> **GET '/questions'**

This endpoint fetches a dictionary of questions available.

**Request Arguments:** 
- *None*

**Returns:** The return should include an success: True message along with the amount of questions available, the categories and current_category.
It should also include an object with a single key, questions, that contains a object of id: question_string key:value pairs, like this:

```javascript
{'2' : "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
'4' : "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
'5' : "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
'5' : "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
'9' : "SWhat boxer's original name is Cassius Clay?"}
```
***
<h4 id="getQuestions2"></h4>

> **GET '/categories/"id"/questions'**

This endpoint fetches a dictionary of questions available for a specific category.

**Request Arguments:** 
- *id* (integer) of the category

**Returns:** The return should include an success: True message along with the amount of questions available on that category and current_category.
It should also include an object with a single key, questions, that contains a object of id: question_string key:value pairs. 

For example, for category id=1, response should look something like this:

```javascript
{'21' : "Who discovered penicillin?",
'22' : "Hematology is a branch of medicine involving the study of what?",
'20' : "What is the heaviest organ in the human body?",
}
```
***
<h4 id="deleteQuestion"></h4>

> **DELETE '/questions/"id"'**

This endpoint allows you to delete a question, based on its id.

**Request Arguments:** 
- *id* (integer) of the question to delete.

**Returns:** An object with a success message, the id of the question deleted and the new amount of questions avaibale. 

For example, for question id=1, if we had 21 questions, response should look somethinkg like this:

```javascript
{'success' : True,
'deleted' : 1,
'total_questions' : 20,
}
```
***
<h4 id="createQuestion"></h4>

> **POST '/questions'**

This endpoint allows you to POST a new question.

**Request Arguments:** 
- *question* (Text)
- *answer* (Text)
- *difficulty* (integer) 1 to 4.
- *category* (integer) 1 to 6.

**Returns:** An object with a success message, the id of the question created and the new amount of questions avaibale. 

For example, for question id=1, if we had 21 questions, response should look somethinkg like this:

```javascript
{'success' : True,
'created' : 25,
'total_questions' : 21,
}
```
***
<h4 id="searchQuestion"></h4>

> **POST '/questions/search'**

This endpoint allows you to search for a question based on a search term, it is case sensitive.

**Request Arguments:** 
- *search_term* (Text)

**Returns:** An object with a success message, the questions that match the criteria and the amount of these questions. 

For example, for search_term='title', response should look somethinkg like this:

```javascript
{'success' : True,
'questions' : [Question1,Question2],
'total_questions' : 2,
}
```
***
<h4 id="postQuizzes"></h4>

> **POST '/quizzes'**

This endpoint allows you to play the game by getting a random question.

**Request Arguments:** 
- *None*

**Returns:** An object with a success message and the new random question: It response should look somethinkg like this:

```javascript
{'success' : True,
'questions' : 'some random question'
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
