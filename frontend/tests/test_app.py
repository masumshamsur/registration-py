import sys
import os
import unittest
from unittest.mock import patch

# Add the frontend/src path to sys.path so we can import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import app  # import your Flask app


class FrontendAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form', response.data)  # Assuming index.html contains a form

    @patch('requests.post')
    def test_submit_form_success(self, mock_post):
        mock_post.return_value.status_code = 200
        response = self.app.post('/submit', data={
            'firstname': 'John',
            'lastname': 'Doe',
            'country': 'USA',
            'gender': 'Male'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John', response.data)

    def test_submit_form_missing_fields(self):
        response = self.app.post('/submit', data={
            'firstname': '',
            'lastname': 'Doe',
            'country': 'USA',
            'gender': 'Male'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Error: All fields are required', response.data)

    @patch('requests.get')
    def test_users_route_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'users': [
                {'id': 1, 'firstname': 'Alice', 'lastname': 'Smith', 'country': 'Canada', 'gender': 'Female'}
            ]
        }
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alice', response.data)

    @patch('requests.delete')
    def test_delete_user_success(self, mock_delete):
        mock_delete.return_value.status_code = 200
        response = self.app.delete('/delete/1')
        self.assertEqual(response.status_code, 302)  # Redirect after delete

    @patch('requests.delete')
    def test_delete_user_failure(self, mock_delete):
        mock_delete.return_value.status_code = 404
        mock_delete.return_value.text = "User not found"
        response = self.app.delete('/delete/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

if __name__ == '__main__':
    unittest.main()
