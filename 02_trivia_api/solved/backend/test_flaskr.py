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
        self.database_path = "postgresql://@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

    
        

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # test for create question with success 
    def test_create_question(self):
        response = self.client().post('/questions', json={"question": "Name three cities in Saudi Araibia", 
            "answer":"Riyadh, Jeddah , Abha",
            "category":1, 
            "difficulty":3})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    # test for create question with fail 
    def test_create_question_fail(self):
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
    # test for get question with success 
    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
    # test for get question with fail 
    def test_get_question_fail(self): 
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
    # test delete function success
    def test_delete_question(self):
        question = Question(
            question="Name three cities in Saudi Araibia", 
            answer="Riyadh, Jeddah , Abha",
            category=1, 
            difficulty=3)
        question.insert()
        id = question.id
        response = self.client().delete('/questions/{}'.format(id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    # test delete function success
    def test_delete_question_fail(self):
        response = self.client().delete('/questions/{}'.format(1000))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    #test search function success
    def test_search(self):
        response = self.client().post('/questions', json={"searchTerm": "Na"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_matching_questions'] > 0)
    #test search function fail
    def test_search_fail(self):
        response = self.client().post('/questions', json={"searchTerm": "N###"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    #test get questions based on category success
    def test_get_question_inCategory(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    #test get questions based on category fail
    def test_get_question_inCategory_fail(self):
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
    #test get category success
    def test_get_category(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['category']) > 0)
        self.assertEqual(data['success'], True)
    #test quiz success
    def test_quiz(self):
        response = self.client().post('/quizzes',json={'previous_questions': [10, 11],'quiz_category': {'type': 'test cat', 'id': '1'}})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
    #test quiz fail
    def test_quiz_fail(self):
        response = self.client().post('/quizzes',json={})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()