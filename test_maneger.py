from loginpage import app
import unittest




class FlaskTestCase2(unittest.TestCase):

    def test_index(self):
        tester=app.test_client(self)
        response=tester.get('/index',content_type='html/text')
        self.assertEqual(response.status_code,404)


    def test_managerpage_page_loads(self):
        tester=app.test_client(self)
        response=tester.get('/managerpage/login',content_type='html/text')
        self.assertTrue((b'Username' in response.data) and (b'Password' in response.data))



    def test_incorrect_login_managerpage(self):
        tester=app.test_client(self)
        response=tester.post('/managerpage/login',data=dict(uname="wrong",psw="wrong"),follow_redirects=True)
        self.assertIn(b'The inputs you put are not correct',response.data)


    def test_correct_login_managerpage(self):
        tester=app. test_client(self)
        response=tester.post('/managerpage/login',data=dict(uname="adam",psw="12345"),follow_redirects=True)
        self.assertIn(b'workers details',response.data)# and (b'report',response.data)# and (b'product finish time',response.data))#and (b'product finish time',response.data)

    def test_correct_login_managerpage123(self):
        tester=app. test_client(self)
        response=tester.post('/managerpage/login',data=dict(uname="adam",psw="12345"),follow_redirects=True)
        self.assertIn(b'report',response.data)






    #def test_correct_login_managerpage13(self):
    #    tester=app.test_client(self)
    #    response=tester.get('/managerpage/coffeeshop',content_type='html/text')
    #    self.assertTrue(b'report'in response.data)

#    def test_correct_login_managerpage_productss(self):
#        tester=app.test_client(self)
#        response=tester.get('/managerpage/coffeeshop',content_type='html/text')
#        self.assertTrue(b'report' in response.data)

#    def test_correct_login_managerpage13(self):
#        tester=app. test_client(self)
#        response=tester.get('/managerpage/productss',content_type='html/text')
#        self.assertTrue(b'product name' in response.data)

#    def test_correct_login_managerpage_productss1(self):
#        tester=app.test_client(self)
#        response=tester.post('/managerpage/login',data=dict(uname="hosam",psw="12345"),follow_redirects=True)
#        self.assertIn(b'product name',response.data) #and (b'product finish time',response.data)

if __name__ == '__main__':
    unittest.main()
