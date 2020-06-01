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

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Reference

### Getting started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: bad request
- 404: resource not found
- 405: method not allowed
- 422: unprocessable
- 500: internal server error

### Endpoints

#### GET /categories
- Fetches a list of strings corresponding to category names, and a success value
- Sample request: `curl http://127.0.0.1:5000/categories`
- Sample response: 
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "success": true
}
``` 

#### GET /questions
- Fetches a list of question objects, success value, total number of questions, a list of current categories, and a list of all category names
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1
- Sample request: `curl http://127.0.0.1:5000/questions?page=2`
- Sample response:
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": [
    0, 
    1, 
    2, 
    3, 
    4, 
    5
  ], 
  "questions": [
    {
      "answer": "Mona Lisa", 
      "category": 1, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 1, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 1, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 0, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 0, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 0, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 3, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Yes it is", 
      "category": 3, 
      "difficulty": 2, 
      "id": 24, 
      "question": "This is a test"
    }, 
    {
      "answer": "Yes it is", 
      "category": 1, 
      "difficulty": 3, 
      "id": 25, 
      "question": "Is this a test question?"
    }, 
    {
      "answer": "Yes it is", 
      "category": 1, 
      "difficulty": 3, 
      "id": 26, 
      "question": "Is this a test question?"
    }
  ], 
  "success": true, 
  "total_questions": 34
}
```

#### DELETE /questions/{question_id}
- Deletes the question of the given id if it exists
- Returns success value, total questions, a question list based on current page number, a list of current categories and a list of categories.
- Sample request: `curl -X DELETE http://127.0.0.1:5000/questions/10?page=2`
- Sample response:
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": [
    0, 
    1, 
    2, 
    3, 
    4, 
    5
  ], 
  "questions": [
    {
      "answer": "One", 
      "category": 1, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 1, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 0, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 0, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 0, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 3, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Yes it is", 
      "category": 3, 
      "difficulty": 2, 
      "id": 24, 
      "question": "This is a test"
    }, 
    {
      "answer": "Yes it is", 
      "category": 1, 
      "difficulty": 3, 
      "id": 25, 
      "question": "Is this a test question?"
    }, 
    {
      "answer": "Yes it is", 
      "category": 1, 
      "difficulty": 3, 
      "id": 26, 
      "question": "Is this a test question?"
    }, 
    {
      "answer": "Yes it is", 
      "category": 1, 
      "difficulty": 3, 
      "id": 27, 
      "question": "Is this a test question?"
    }
  ], 
  "success": true, 
  "total_questions": 33
}
```

#### POST /questions
Can serve 2 purposes:
1. Creates a new question using the submitted question, category, answer and difficulty if in payload of request.
    1. Returns success value, total questions, a question list based on current page number, a list of current categories and a list of categories.
    2. Sample request: `curl -X POST  http://127.0.0.1:5000/questions?page=4 -H "Content-Type: application/json" -d '{"question": "Is this a test question?", "answer": "Yes it is", "category": 2, "difficulty": 3}'`
    3. Sample response:
    ```
    {
      "categories": [
        "Science", 
        "Art", 
        "Geography", 
        "History", 
        "Entertainment", 
        "Sports"
      ], 
      "current_category": [
        0, 
        1, 
        2, 
        3, 
        4, 
        5
      ], 
      "questions": [
        {
          "answer": "Hist", 
          "category": 3, 
          "difficulty": 5, 
          "id": 38, 
          "question": "History question"
        }, 
        {
          "answer": "Ent", 
          "category": 4, 
          "difficulty": 4, 
          "id": 39, 
          "question": "Entertainmnt question"
        }, 
        {
          "answer": "Sport", 
          "category": 5, 
          "difficulty": 2, 
          "id": 40, 
          "question": "Sports question"
        }, 
        {
          "answer": "Yes it is", 
          "category": 2, 
          "difficulty": 3, 
          "id": 41, 
          "question": "Is this a test question?"
        }
      ], 
      "success": true, 
      "total_questions": 34
    }
   ```
2. Searches questions that have a certain search term in them if searchTerm is in payload
    1. Search is case insensitive
    2. Returns success value, total questions that have the search term, a list of quetions with the search term based on current page number, a list of current categories and a list of categories.
    3. Sample request: `curl -X POST  http://127.0.0.1:5000/questions?page=1 -H "Content-Type: application/json" -d '{"searchTerm": "anne"}'`
    4. Sample response:
    ```
   {
     "categories": [
       "Science", 
       "Art", 
       "Geography", 
       "History", 
       "Entertainment", 
       "Sports"
     ], 
     "current_category": [
       4
     ], 
     "questions": [
       {
         "answer": "Tom Cruise", 
         "category": 4, 
         "difficulty": 4, 
         "id": 4, 
         "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
       }
     ], 
     "success": true, 
     "total_questions": 1
   }
   ``` 

#### GET /categories/{category_id}/questions
- Fetches a list of question objects, success value, total number of questions, a list of current categories, and a list of all category names, for questions in a specific category
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1
- Sample request: `curl http://127.0.0.1:5000/categories/2/questions?page=1`
- Sample response:
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": [
    2
  ], 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 2, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 2, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 2, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "aaaa", 
      "category": 2, 
      "difficulty": 2, 
      "id": 28, 
      "question": "This is a test"
    }, 
    {
      "answer": "hhhh", 
      "category": 2, 
      "difficulty": 4, 
      "id": 29, 
      "question": "History question"
    }, 
    {
      "answer": "Geo", 
      "category": 2, 
      "difficulty": 3, 
      "id": 37, 
      "question": "Geography question"
    }, 
    {
      "answer": "Yes it is", 
      "category": 2, 
      "difficulty": 3, 
      "id": 41, 
      "question": "Is this a test question?"
    }
  ], 
  "success": true, 
  "total_questions": 7
}
```

#### POST /quizzes
- Returns a random question and success value from a specific category that isn't in a list of previous question ids
- Sample request: `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category": {"type": "Science", "id":0}, "previous_questions": [35,21]}'`
- Sample response:
```
{
  "question": {
    "answer": "The Liver", 
    "category": 0, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
```
To request a next question of any category, specify "id": 0 and "type": "click" in quiz_category

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```