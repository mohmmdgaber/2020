from loginpage import app
import unittest


class FlaskTestCase(unittest.TestCase):
    def test_index(self):
        tester=app.test_client(self)
        response=tester.get('/index',content_type='html/text')
        self.assertEqual(response.status_code,404)

    def test_worker_page_loads(self):
        tester=app.test_client(self)
        response=tester.get('/worker/login',content_type='html/text')
        self.assertTrue((b'Username' in response.data)and(b'Password' in response.data)and (b'Enter The coffeeshop name' in response.data))

    def test_correct_login_worker(self):
        tester=app.test_client(self)
        response=tester.post('/worker/login',data=dict(uname="hosam",psw="12345",coffeeshop="12345"),follow_redirects=True)
        self.assertIn(b'finish time',response.data) and (b'order',response.data) and (b'name',response.data)and(b'NAVBAR',response.data)

    def test_incorrect_login_worker(self):
        tester=app.test_client(self)
        response=tester.post('/worker/login',data=dict(uname="wrong",psw="wrong",coffeeshop="wrong"),follow_redirects=True)
        self.assertIn(b'The inputs you put are not correct',response.data)


if __name__ == '__main__':
    unittest.main()
