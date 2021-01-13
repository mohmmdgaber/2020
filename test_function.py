import  unittest
import  math
from manager.managerpages import validhours
from manager.managerpages import validdays
from manager.managerpages import validcode
from manager.managerpages import allowed_image
from manager.managerpages import intime
from orders.orderpage import validcoupon
class TestMathOperations(unittest.TestCase):

    # maneger
    def test_validhours(self):
        self.assertEqual(validhours(12,13),True,"start < end")
        self.assertNotEqual(validhours(15,13),True,"start < end")


    def test_validdays(self):
        self.assertEqual(validdays(12,13),True,"start < end")
        self.assertNotEqual(validdays(15,13),True,"start < end")


    def test_validcode(self):
        self.assertEqual(validcode("Asqw1","1","12"),False)
        self.assertNotEqual(validcode("Asqw1","13","dawd"),True)


    def test_allowed_image(self):
        self.assertEqual(allowed_image("Name"),False)
        self.assertNotEqual(allowed_image("Name"),True)


    def test_intime(self):
        self.assertEqual(intime(1,24,0,6),True)
        self.assertNotEqual(intime(1,24,6,1),True)




#order

    def test_validcoupon(self):
        self.assertEqual(validcoupon("",123456789),False)
        self.assertNotEqual(validcoupon("",1233435),True)




if __name__ == '__main__':
    unittest.main()
