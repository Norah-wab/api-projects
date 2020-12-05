# Project description
this project is a game where end users play and test thier knowledge at the same time by answering travia questions, the features this project are:-
1- display question based on selected category or get all questions. 
2- add questions. 
3- delete question. 
4- search for specific question. 
5- play quiz which you will get question after another one then score displayed. 
# Project dependencies
To run this project you will need the following to installed:- 
1- python3 
2- pip 
3- node
4- npm 
# Start backend
1- go to folder: 02_trivia_api/solved/backend. 
2- using command line run this command: pip install -r requirements.txt. 
3- using command line run this command: 
    dropdb trivia
    createdb trivia
4- after installing dependency you can run the server using these commands: 
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run
# Start frontend
1- go to folder: 02_trivia_api/solved/frontend
2- using command line run this command: npm init. 
3- using command line run this command: npm start. 
4- in browser open: http://localhost:3000. 

# To test backend 
1- on command line run this command: 
    dropdb trivia_test
    createdb trivia_test
2- then run this command:
    python3 test_flaskr.py
# API refrence
 URL: http://localhost:5000/
# End point 
1- http://localhost:5000/categories GET
    purpose: end point to get list of categories
    request: http://localhost:5000/categories
    response:
    {
        "category": {
            "1": "Math",
            "2": "Social"
        },
        "success": true
    }
2- http://localhost:5000/questions GET
    purpose: end point to get list of questions
    request: http://localhost:5000/questions?page=2
    response:
    {
    "categories": [
        {
            "id": 1,
            "type": "Math"
        },
        {
            "id": 2,
            "type": "Social"
        }
        ],
    "current_category": null,
    "questions": [
        {
            "answer": "answer1",
            "category": "2",
            "difficulty": 5,
            "id": 1,
            "question": "question1"
        },
        {
            "answer": "answer2",
            "category": "2",
            "difficulty": 5,
            "id": 2,
            "question": "question2"
        }
    ],
    "success": true,
    "totalQuestions": 2
    }
3- http://localhost:5000/questions/<int:question_id>  Delete
    purpose: end point to delete specific question  
    request: http://localhost:5000/questions/1
    response:
        {
            "deleted": 1,
            "success": true
        }
4- http://localhost:5000/questions POST
    purpose: end point to create new question or search for specific question based on request. 
    request: 
        * to create question 
            {
                "question": "Name three cities in Saudi Araibia",
                "answer": "Riyadh, Jeddah , Abha",
                "difficulty": 4,
                "category": "1"
            }
        * to search for question 
          {
            "searchTerm": "Na"
          }
    response:
        * to create question 
        {
            "success": true
        }
        * to search for question 
        {
            "questions": 
            [
                {
                    "answer": "Riyadh, Jeddah , Abha",
                    "category": "1",
                    "difficulty": 4,
                    "id": 19,
                    "question": "Name three cities in Saudi Araibia"
                }
            ],
        "search_term": "Na",
        "success": true,
        "total_matching_questions": 1,
        "total_questions": 4
        }

5- http://localhost:5000/categories/<int:category_id>/questions GET
    purpose: end point to get questions in specific category. 
    request: http://localhost:5000/categories/1/questions
    response:
        {
            "current_category": 
            {
            "id": 1,
            "type": "Math"
            },
            "questions": 
        [
        {
            "answer": "20",
            "category": "1",
            "difficulty": 1,
            "id": 3,
            "question": "5*4"
        },
        {
            "answer": "12",
            "category": "1",
            "difficulty": 4,
            "id": 4,
            "question": "8+4"
        }
        ],
        "success": true,
        "total_in_category": 2,
        "total_questions": 4
    }
6- http://localhost:5000/quizzes POST
    purpose: end point to play and get questions one after other after choosing the category. 
    request: 
        {
         "previous_questions": [],
         "quiz_category": {"type": "Math", "id": "1"}
         }
    response:
    {
    "question": {
            "answer": "20",
            "category": "1",
            "difficulty": 1,
            "id": 3,
            "question": "5*4"
        },
    "success": true
}
# Error handling 
using trivia API you may recieve one of these:
    * 404 –-> Not found
    * 422 –-> UNPROCESSABLE
    * 405 –-> Method not allowed
    * 400 --> Bad request 
in this format: 
    {
        "error": error code,
        "message": Message,
        "success": false
    }