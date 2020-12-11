

class user :

    def __init__(self,name,password):
        self.name=name
        self.password=password
    def checklogin(self,name,password):
        if(self.name=='true' and self.password=='true' ) :
            return 1
        else:
            return 0
    def printmassege(self):

         if(user.checklogin(getname(),getpassword())==0):
            print("the inputs u entered are incorrect/don't match the database")

    def getnameuser(self):
        return self.nameuser

    def getpassword(self):
        return self.password



class manager(user):
            def __init__(self, name, password, coffeeshopname):
                self.name = name
                self.password = password
                self.coffeeshopname = coffeeshopname

            def getname(self):
                return self.name

            def getpassword(self):
                return self.password

            def getcoffeeshopname(self):
                return self.coffeeshopname

def getname(self):

   return self.name
def getpassword(self):
    return self.password

