from flask import Blueprint,redirect, url_for, render_template,request,session,flash,current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
managerpage=Blueprint('managerpage', __name__, template_folder='templates',static_folder='static')

def allowed_image(filename):
    if not "." in filename:
        return False
    ext=filename.rsplit(".",1)[1]
    if ext.upper() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def validhours(start,end):
    if start>end or start==end:
         return False
    else:
         return True
def validdays(start,end):
    if start>end:
         return False
    else:
         return True
def validcode(code,uses,discount):
    if not (uses.isdigit() and discount.isdigit()):
        return False
    if len(code)>5 and int(uses) >0 and int(discount)>0:
        return True
    return False
def intime(starthour,endhour,startday,endday):
        dayoftheweek=int(datetime.now().strftime('%w'))
        hour=datetime.now().hour
        print(hour)
        print(dayoftheweek)
        print(starthour,endhour,startday,endday)

        if (starthour<=hour and endhour>=hour) and (startday<=dayoftheweek and endday>=dayoftheweek):
            return True
        else:
            return False

def whatmanagers():
    for i in managers.query.all():
        if intime(i.starthour,i.endhour,i.startday,i.endday)==True:
            print("This counts?")
            i.isthestoreopen=True
            for j in i.workers:
                if intime(j.starthour,j.endhour,j.startday,j.endday)==True:
                      j.isinshift=True
                else:
                      j.isinshift=False

        else:
            print("This doesn't counts?")
            i.isthestoreopen=False
            for j in i.workers:
                 j.isinshift=False


    db.session.commit()

def shopscope(manager,starthour,endhour,startday,endday):
        if (manager.starthour<=starthour and manager.endhour>=endhour) and (manager.startday<=startday and manager.endday>=endday):
                return True
        else:
                return False


db=SQLAlchemy()


class managers(db.Model):
        __bind_key__='managers'
        id=db.Column("id",db.Integer,primary_key=True)
        name=db.Column(db.String(100))
        password=db.Column(db.String(100))
        coffeeshop=db.Column(db.String(100))
        revenue=db.Column(db.Integer)
        sales=db.Column(db.Integer)
        starthour=db.Column(db.Integer)
        endhour=db.Column(db.Integer)
        startday=db.Column(db.Integer)
        endday=db.Column(db.Integer)
        onestar=db.Column(db.Integer)
        twostar=db.Column(db.Integer)
        threestar=db.Column(db.Integer)
        fourstar=db.Column(db.Integer)
        fivestar=db.Column(db.Integer)
        lateststate=db.Column(db.String(2000))
        isthestoreopen=db.Column(db.Boolean)
        bitcoinadress=db.Column(db.String)
        workers = db.relationship('workers', backref='managers')
        products=db.relationship('products',backref='managers')
        coupons=db.relationship('coupons',backref='managers')




class workers(db.Model):
   __bind_key__='workers'
   id=db.Column("id",db.Integer,primary_key=True)
   name=db.Column(db.String(100))
   password=db.Column(db.String(100))
   starthour=db.Column(db.Integer)
   endhour=db.Column(db.Integer)
   startday=db.Column(db.Integer)
   endday=db.Column(db.Integer)
   isinshift=db.Column(db.Boolean)
   workerlatestmessage=db.Column(db.String(2000))
   managers_id=db.Column(db.Integer,db.ForeignKey('managers.id'))
   tips=db.Column(db.Integer)

class products(db.Model):
      __bind_key__='products'
      id=db.Column("id",db.Integer,primary_key=True)
      name=db.Column(db.String(100))
      quantity=db.Column(db.Integer)
      price=db.Column(db.Integer)
      expitingdate=db.Column(db.Date)
      mimetype=db.Column(db.Text,nullable=False)
      imagename=db.Column(db.String(100))
      catageory=db.Column(db.String(100))
      finishtime= db.Column(db.Integer)
      instruction=db.Column(db.String(2000))
      managers_id=db.Column(db.Integer,db.ForeignKey('managers.id'))
class coupons(db.Model):
       __bind_key__='coupons'
       id=db.Column("id",db.Integer,primary_key=True)
       code=db.Column(db.String(100))
       expirationdate=db.Column(db.Date)
       uses=db.Column(db.Integer)
       fulluses=db.Column(db.Integer)
       discount=db.Column(db.Integer)
       managers_id=db.Column(db.Integer,db.ForeignKey('managers.id'))

class orders(db.Model):
    __bind_key__='orders'
    id=db.Column("id",db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    ordertime=db.Column(db.Integer)
    sales=db.Column(db.Integer)
    time=db.Column(db.DateTime)
    fullprice=db.Column(db.Integer)
    tipamount=db.Column(db.Integer)
    discount=db.Column(db.Integer)
    managerid=db.Column(db.Integer)
    valid=db.Column(db.Boolean)
    workerid=db.Column(db.Integer)
    selectedorders= db.relationship('selectedorders', backref='orders')

class selectedorders(db.Model):
      __bind_key__='selectedorders'
      id=db.Column("id",db.Integer,primary_key=True)
      name=db.Column(db.String(100))
      price=db.Column(db.Integer)
      instruction=db.Column(db.String(2000))
      orders_id=db.Column(db.Integer,db.ForeignKey('orders.id'))
      productid=db.Column(db.Integer)
      quantity=db.Column(db.Integer)

@managerpage.route("/")
def home():
    db.create_all()
    return redirect(url_for("managerpage.login"))



@managerpage.route("/login",methods=["POST","GET"])
def login():
    if "manager" in session:
        return redirect(url_for("managerpage.coffeeshop"))
    if request.method=="POST":
        userr=request.form["uname"]
        password=request.form["psw"]
        found=managers.query.filter_by(name=userr).first()

        if found:
          if found.password==password:
               session["manager"]=found.id
               return redirect(url_for("managerpage.coffeeshop"))
          else:
               return render_template("login.html",content="The inputs you put are not correct")
        else:
            return render_template("login.html",content="The inputs you put are not correct")

    else:
        return render_template("login.html")

@managerpage.route("/coffeeshop",methods=["POST","GET"])
def coffeeshop():
    if "manager" not in session:
        return 'error',400
    found=managers.query.filter_by(id=session["manager"]).first()
    dayss=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    if request.method=="POST":
       starthour=int(request.form.get("starthour"))
       endhour=int(request.form.get("endhour"))
       startday=int(request.form.get("startday"))
       endday=int(request.form.get("endday"))
       if not(validhours(starthour,endhour) and validdays(startday,endday)):
           return 'Error',400
       found.starthour=starthour
       found.endhour=endhour
       found.startday=startday
       found.endday=endday
       db.session.commit()
       print(startday)
       print(found.startday)
       return render_template("manager.html",value=found.workers,sales=found.sales,revenue=found.revenue,days=dayss,manager=found)

    return render_template("manager.html",value=found.workers,sales=found.sales,revenue=found.revenue,days=dayss,manager=found)


@managerpage.route("/workerss",methods=["POST","GET"])
def workerss():
    foundmanager=managers.query.filter_by(id=session["manager"]).first()
    dayss=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    if request.method=="POST":
       workername=request.form["workername"]
       workerpassword=request.form["workerpassword"]
       starthour=int(request.form.get("starthour"))
       endhour=int(request.form.get("endhour"))
       startday=int(request.form.get("startday"))
       endday=int(request.form.get("endday"))
       if  request.form.get("add"):
           if not validhours(starthour,endhour):
              return render_template("addworker.html",value=foundmanager.workers,days=dayss,message='*incorrect hours input')
           if not validdays(startday,endday):
              return render_template("addworker.html",value=foundmanager.workers,days=dayss,message='*incorrect days input')
           if not shopscope(foundmanager,starthour,endhour,startday,endday):
               return render_template("addworker.html",value=foundmanager.workers,days=dayss,message='*not in the scope of the shops working hours')


           workerrr=workers(name=workername,password=workerpassword,starthour=starthour,endhour=endhour,startday=startday,endday=endday,managers_id=foundmanager.id,tips=0)
           db.session.add(workerrr)
           db.session.commit()

           return render_template("addworker.html",value=foundmanager.workers,days=dayss)

       elif  request.form.get("remove"):
           found=workers.query.filter_by(managers_id=session["manager"],name=request.form["workername"]).first()
           if not found:
                   return render_template("addworker.html",value=foundmanager.workers,days=dayss,message='*incorrect name input')
           db.session.delete(found)
           db.session.commit()
           return render_template("addworker.html",value=foundmanager.workers,days=dayss)
       elif  request.form.get("update"):
            found=workers.query.filter_by(managers_id=session["manager"],name=request.form["workername"]).first()
            if  not found:
                return render_template("addworker.html",value=foundmanager.workers,days=dayss,message='*incorrect name input')
            if  request.form["workerpassword"]!='':
               found.password=request.form["workerpassword"]
            if  validhours(starthour,endhour) and shopscope(foundmanager,starthour,endhour,startday,endday) :
                found.starthour=starthour
                found.endhour=endhour
            else:
                return render_template("addworker.html",value=foundmanager.workers,days=dayss,message='*not in the scope of the shops working hours')
            if  validdays(startday,endday) and shopscope(foundmanager,starthour,endhour,startday,endday):
                found.starday=startday
                found.endday=endday
            else:
                 return render_template("addworker.html",value=foundmanager.workers,days=dayss,message='*not in the scope of the shops working hours')

            db.session.commit()
            return render_template("addworker.html",value=foundmanager.workers,days=dayss)
    else:
        found=managers.query.filter_by(id=session["manager"]).first()
        return render_template("addworker.html",value=found.workers,days=dayss)

@managerpage.route("/productss",methods=["POST","GET"])
def productss():
     foundmanager=managers.query.filter_by(id=session["manager"]).first()
     if request.method=="POST":
        if request.form.get("add"):
           pic = request.files['pic']
           productname=request.form['productname']
           productquantity=request.form['productquantity']
           productprice=request.form['productprice']
           productexpiringdate = datetime.strptime(request.form['productexpiringdate'],'%Y-%m-%d')
           productcatageory=request.form.get('productcatageory')
           productfinishtime=request.form['productfinishtime']
           productinstruction=request.form['instruction']
           if not pic:
              return 'No pic uploaded!', 400

           mimetype = pic.mimetype
           if  not mimetype or pic.filename =="":
              return 'Bad upload!', 400
           if  not (allowed_image(pic.filename)):
                 return 'Bad upload!', 400
           product = products(name=productname, mimetype=mimetype,quantity=int(productquantity),expitingdate=productexpiringdate,managers_id=foundmanager.id,price=int(productprice),catageory=productcatageory,finishtime=int(productfinishtime),instruction=productinstruction)
           db.session.add(product)
           db.session.commit()
           product.imagename=(str(product.id)+'.'+(pic.filename.rsplit(".",1)[1]))
           db.session.commit()
           pic.save(os.path.join(current_app.config["IMAGE_UPLOADS"],product.imagename))
           return render_template("productmanager.html",value=foundmanager.products)
        elif request.form.get("remove"):
            found=products.query.filter_by(managers_id=session["manager"],name=request.form["productname"]).first()
            os.remove(os.path.join(current_app.config["IMAGE_UPLOADS"], found.imagename))
            db.session.delete(found)
            db.session.commit()
            return render_template("productmanager.html",value=foundmanager.products)
        elif request.form.get("update1"):
            found=products.query.filter_by(managers_id=session["manager"],name=request.form["productname"]).first()
            if request.form['productquantity'] =='' or found==None:
                 return 'Bad inputs!', 400
            found.quantity=request.form['productquantity']
            db.session.commit()
            return render_template("productmanager.html",value=foundmanager.products)

        elif request.form.get("update2"):
            found=products.query.filter_by(managers_id=session["manager"],name=request.form["productname"]).first()
            if found==None:
                     return 'Bad inputs!', 400
            found.expitingdate=datetime.strptime(request.form['productexpiringdate'],'%Y-%m-%d')
            db.session.commit()
            return render_template("productmanager.html",value=foundmanager.products)


        elif request.form.get("update3"):
            found=products.query.filter_by(managers_id=session["manager"],name=request.form["productname"]).first()
            productprice=request.form['productprice']
            if productprice =='' or found==None:
                 return 'Bad inputs!', 400
            found.price=int(productprice)
            db.session.commit()
            return render_template("productmanager.html",value=foundmanager.products)

     else:
           return render_template("productmanager.html",value=foundmanager.products)


@managerpage.route("/couponss",methods=["POST","GET"])
def couponss():
        foundmanager=managers.query.filter_by(id=session["manager"]).first()
        if request.method=="POST":
               code=request.form['code']
               uses=request.form['uses']
               expiringdate=datetime.strptime(request.form['expiringdate'],'%Y-%m-%d')
               discount=request.form['discount']
               if request.form.get("add"):
                   if not validcode(code,uses,discount):
                          return render_template("copone.html",message="not a valid code or number of uses or a discount ammount",value=foundmanager.coupons)
                   if coupons.query.filter_by(managers_id=foundmanager.id,code=request.form["code"]).first():
                         return render_template("copone.html",message="There's an already existing coupon with the same code",value=foundmanager.coupons)
                   found=coupons(code=code,fulluses=int(uses),uses=0,expirationdate=expiringdate,discount=int(discount),managers_id=foundmanager.id)
                   db.session.add(found)
                   db.session.commit()
                   return render_template("copone.html",message="A coupon got added",value=foundmanager.coupons)

               elif  request.form.get("remove"):
                   found=coupons.query.filter_by(managers_id=foundmanager.id,code=code).first()
                   if not found:
                         return render_template("copone.html",message="There's no coupon with the mathcing code to delete",value=foundmanager.coupons)
                   db.session.delete(found)
                   db.session.commit()
                   return render_template("copone.html",message="A coupon got deleted",value=foundmanager.coupons)
               elif  request.form.get("update"):
                    found=coupons.query.filter_by(managers_id=foundmanager.id,code=request.form["code"]).first()
                    if  not found:
                        return render_template("copone.html",message="There's no coupon with the mathcing code to update",value=foundmanager.coupons)
                    if  uses !='':
                       found.fulluses=int(uses)
                    if discount!='':
                        found.discount=int(discount)
                    db.session.commit()
                    return render_template("copone.html",message="A coupon got updated",value=foundmanager.coupons)

        else:
              return render_template("copone.html",message="Enter a code that's longer than 10 characters and a number of uses that's bigger than 0",value=foundmanager.coupons)
