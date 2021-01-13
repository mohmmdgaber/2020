from flask import Blueprint,redirect, url_for, render_template,request,session,flash,current_app
from flask_sqlalchemy import SQLAlchemy
from manager.managerpages import managers
from manager.managerpages import workers
from manager.managerpages import orders
from manager.managerpages import products
from manager.managerpages import selectedorders

worker=Blueprint('worker', __name__, template_folder='templates',static_folder='static')
db=SQLAlchemy()

@worker.route("/")
def home():
    db.create_all()
    return redirect(url_for("worker.login"))

@worker.route("/login",methods=["POST","GET"])
def login():
    if "worker" in session:
        return redirect(url_for("worker.coffeeshop"))
    if request.method=="POST":
        userr=request.form["uname"]
        password=request.form["psw"]
        coffeeshop=request.form["coffeeshop"]
        manager=managers.query.filter_by(coffeeshop=coffeeshop).first()
        if manager==None:
            return render_template("loginworker.html",content="The inputs you put are not correct")
        found=workers.query.filter_by(name=userr,managers_id=manager.id).first()
        if found:
          if found.password==password:
               session["worker"]=found.id
               return redirect(url_for("worker.coffeeshop"))
          else:
               return render_template("loginworker.html",content="The inputs you put are not correct")
        else:
            return render_template("loginworker.html",content="The inputs you put are not correct")

    else:
        return render_template("loginworker.html")

@worker.route("/coffeeshop",methods=["POST","GET"])
def coffeeshop():
    if request.method=="POST":
       orderz=db.session.query(orders).filter_by(workerid=session["worker"],valid=True).all()
       orderzz=db.session.query(orders).filter_by(workerid=session["worker"],valid=False).all()
       for i in orderzz:
            if request.form.get("valid"+str(i.id)):
                print("innnnntoopp")

                order=db.session.query(orders).filter_by(id=i.id,workerid=session["worker"]).first()
                price=0
                if order.discount*2<order.fullprice:
                    price=order.fullprice-order.discount

                price=price+order.tipamount
                manager=db.session.query(managers).filter_by(id=order.managerid).first()
                worker=db.session.query(workers).filter_by(id=order.workerid).first()
                manager.sales=order.sales+manager.sales
                manager.revenue=price-order.tipamount
                worker.tips=worker.tips+order.tipamount
                for i in selectedorders.query.filter_by(orders_id=order.id).all():
                   found=db.session.query(products).filter_by(id=i.productid).first()
                   if found:
                       found.quantity=found.quantity-i.quantity
                order.valid=True
                db.session.commit()
                orderzzz=orders.query.filter_by(workerid=session["worker"],valid=False).all()
                orderss=orders.query.filter_by(workerid=session["worker"],valid=True).all()

                return render_template("worker.html",value=orderss,value2=orderzzz)

       for i in orderz:
            if request.form.get("finish"+str(i.id)):
                order=db.session.query(orders).filter_by(id=i.id,workerid=session["worker"]).first()
                db.session.delete(order)
                db.session.commit()
                orderss=orders.query.filter_by(workerid=session["worker"],valid=True).all()
                orderzzz=orders.query.filter_by(workerid=session["worker"],valid=False).all()
                return render_template("worker.html",value=orderss,value2=orderzzz)


    else:
      orderz=db.session.query(orders).filter_by(workerid=session["worker"],valid=True).all()
      orderzzz=db.session.query(orders).filter_by(workerid=session["worker"],valid=False).all()
      return render_template("worker.html",value=orderz,value2=orderzzz)

@worker.route("/emergency",methods=["POST","GET"])
def emergency():
    worker=workers.query.filter_by(id=session["worker"]).first()
    manager=db.session.query(managers).filter_by(id=worker.managers_id).first()
    if request.method=="POST":
        message=request.form.get("idmessage")
        manager.lateststate=message
        db.session.commit()
        return render_template("emergency.html",recentmessage=manager.lateststate)

    else:
       return render_template("emergency.html",manager=manager)


@worker.route("/communication",methods=["POST","GET"])
def communication():
        worker=workers.query.filter_by(id=session["worker"]).first()
        manager=db.session.query(managers).filter_by(id=worker.managers_id).first()
        if request.method =="POST":
            idmessage=request.form.get("idmessage")
            sentworker=db.session.query(workers).filter_by(id=int(request.form.get("workerslist"))).first()
            print(sentworker.name)
            sentworker.workerlatestmessage= worker.name +" :sent to: "+sentworker.name+" The following message: "+"("+idmessage+")"
            db.session.commit()
            shownworker=workers.query.filter_by(id=session["worker"]).first()
            return render_template("communication.html",manager=manager,message=shownworker.workerlatestmessage)



        return render_template("communication.html",manager=manager,message=worker.workerlatestmessage)
