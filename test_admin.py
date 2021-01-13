from loginpage import app
import unittest


class FlaskTestCase(unittest.TestCase):
    def test_index(self):
        tester=app.test_client(self)
        response=tester.get('/index',content_type='html/text')
        self.assertEqual(response.status_code,404)

    def test_admin_page_loads(self):
        tester=app.test_client(self)
        response=tester.get('/admin/',content_type='html/text')
        self.assertTrue((b'This is the page to enter if you' in response.data)and(b're the site adminster to control the whole system' in response.data)and (b'Enter the admin single password' in response.data)and (b'Password' in response.data))

    def test_correct_login_admin(self):
        tester=app.test_client(self)
        response=tester.post('/admin/',data=dict(psw="1234"),follow_redirects=True)
        self.assertIn(b'managerpassword',response.data) and (b'managerpassword',response.data) and (b'managercoffeshop',response.data)and(b'list',response.data)and(b'password',response.data)and(b'coffeeshopname',response.data)and(b'add',response.data)and(b'update',response.data)

    def test_incorrect_login_admin(self):
        tester=app.test_client(self)
        response=tester.post('/admin/',data=dict(psw="wrong"),follow_redirects=True)
        self.assertIn(b'The input is not correct',response.data)


if __name__ == '__main__':
    unittest.main()
