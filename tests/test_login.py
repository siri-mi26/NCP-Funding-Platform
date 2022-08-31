from app import app, db 
from app.models import User
from flask import url_for
from flask_login import current_user
import unittest

"""Run with: python -m unittest tests/test_login.py from top directory
Need to have created a user in the app.db with username:test, and password:test
Will add commands to setUp tomorrow. 
"""
class FlaskLogin(unittest.TestCase): 

    def setUp(self):
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        #app.login_manager._login_disabled = False #doesn't help either
        self.app = app
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

        db.create_all()

    def test_login_loads (self):
        """Test we can get to login page"""
        tester = app.test_client(self)
        response = tester.get('/login', content_type = 'html/text')
        self.assertTrue(b"Sign In" in response.data)


    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_correct_login(self):
        """Test login with correct credentials"""
        with self.client:
            response = self.login('test', 'test')
            #self.assertIn(b'Successfull Login', response.data)
            html = response.get_data(as_text=True)
            #print(html)
            assert response.status_code == 200
            assert 'Hi, test' in html
            self.assertTrue(current_user.username=='test')

    def test_empty_login(self):
        """Test login with correct credentials"""
        with self.client:
            response = self.login('', '')
            #self.assertIn(b'Successfull Login', response.data)
            self.assertIn(b'Sign In', response.data)

    def test_incorrect_login(self):
        """Test login with correct credentials"""
        with self.client:
            response = self.login('test', 'tset')
            response2 = self.login('tset', 'tset')
            #self.assertIn(b'Successfull Login', response.data)
            self.assertIn(b'Sign In', response.data)
            self.assertIn(b'Sign In', response2.data)

    def test_logout(self):
        """Test after successful login we can logout"""
        with self.client:
            self.login('test', 'test')
            response = self.client.get('/logout', follow_redirects=True)
            assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()