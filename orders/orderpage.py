from flask import Blueprint,redirect, url_for, render_template,request,session,flash,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from datetime import datetime
from manager.managerpages import managers
from manager.managerpages import workers
from manager.managerpages import orders
from manager.managerpages import selectedorders
from manager.managerpages import coupons
from manager.managerpages import products
from manager.managerpages import whatmanagers

def fullprice(orderid):
    c=0
    for i in selectedorders.query.filter_by(orders_id=orderid).all():
        c=c+i.quantity*i.price

    return c
def fullsales(orderid):
    c=0
    for i in selectedorders.query.filter_by(orders_id=orderid).all():
        c=c+i.quantity
    return c

def ordertime(orderid):
        d=0
        order=orders.query.filter_by(id=orderid).first()
        for i in products.query.filter_by(managers_id=order.managerid).all():
            found=selectedorders.query.filter_by(name=i.name,orders_id=order.id).first()
            if found:
                d=d+i.finishtime*found.quantity
        return d

def validcoupon(code,orderid):
    if code=="":
        return False
    order=orders.query.filter_by(id=orderid).first()
    coupon=coupons.query.filter_by(managers_id=order.managerid, code=code).first()
    if coupon:
        return True
    else:
        return False




order=Blueprint('order', __name__, template_folder='templates',static_folder='static')
QRcode(current_app)
db=SQLAlchemy()


@order.route("/",methods=["POST","GET"])
def home():
    whatmanagers()
    if request.method=="POST":
        if len(request.form) == 0:
            return render_template("coffeepick.html",value=managers.query.filter_by(isthestoreopen=True).all(),message="Please pick one of the shops")

        else:
         selectedshop=int(request.form['radio'])
         manager=managers.query.filter_by(id=selectedshop).first()
         worker=workers.query.filter_by(managers_id=selectedshop,isinshift=True).first()
         neworder=orders(managerid=selectedshop,workerid=worker.id,discount=0,tipamount=0,valid=False)
         db.session.add(neworder)
         db.session.commit()
         session["order"]=neworder.id
         return redirect(url_for('order.productselection'))
    else:
       if "order" in session:
          found=db.session.query(orders).filter_by(id=session["order"]).first()
          if found:
             for i in  db.session.query(selectedorders).filter_by(orders_id=session["order"]).all():
                  db.session.delete(i)
             db.session.delete(found)
             db.session.commit()
          session.pop("order",None)
       return render_template("coffeepick.html",value=managers.query.filter_by(isthestoreopen=True).all(),message="check")


@order.route("/productselection",methods=["POST","GET"])
def productselection():

          neworder= db.session.query(orders).filter_by(id=session["order"]).first()
          theshop=managers.query.filter_by(id=neworder.managerid).first()
          shownproducts=products.query.filter_by(managers_id=theshop.id).all()
          if request.method=="POST":
             catageory=request.form.get('catageory')
             if catageory!="all":
                 shownproducts=products.query.filter_by(managers_id=theshop.id,catageory=catageory).all()
             else:
                  shownproducts=products.query.filter_by(managers_id=theshop.id).all()
             for i in shownproducts:
                    if request.form.get("add"+str(i.id)):
                        selectionn=db.session.query(selectedorders).filter_by(orders_id=neworder.id,productid=i.id).first()
                        if selectionn:
                            k=selectionn.quantity+int(request.form.get(str(i.id)))
                            if k<=10:
                              selectionn.quantity=k
                            else:
                              selectionn.quantity=10
                              db.session.commit()
                              return render_template("productselection.html",value=shownproducts,message=catageory,warning="maximum of 10 on each item",selection=neworder.selectedorders,price=fullprice(neworder.id))

                        else:
                            newselection=selectedorders(name=i.name,price=i.price,productid=i.id,quantity=request.form.get(str(i.id)),orders_id=neworder.id,instruction=i.instruction)
                            db.session.add(newselection)
                        db.session.commit()
                        return render_template("productselection.html",value=shownproducts,message=catageory,selection=neworder.selectedorders,price=fullprice(neworder.id))
                    elif request.form.get("remove"+str(i.id)):
                        selectionn=db.session.query(selectedorders).filter_by(orders_id=neworder.id,productid=i.id).first()
                        if selectionn:
                            k=selectionn.quantity-int(request.form.get(str(i.id)))
                            if k==0:
                                db.session.delete(selectionn)
                            if k>=1:
                              selectionn.quantity=k
                            else:
                              db.session.delete(selectionn)
                              db.session.commit()
                              return render_template("productselection.html",value=shownproducts,message=catageory,warning="minimmum of 0 on each item",selection=neworder.selectedorders,price=fullprice(neworder.id))

                        db.session.commit()
                        return render_template("productselection.html",value=shownproducts,message=catageory,selection=neworder.selectedorders,price=fullprice(neworder.id))

             if request.form.get("submitt"):
                 neworder.fullprice=fullprice(neworder.id)
                 neworder.sales=fullsales(neworder.id)
                 neworder.ordertime=ordertime(neworder.id)
                 db.session.commit()
                 return redirect(url_for('order.cart'))

             return render_template("productselection.html",value=shownproducts,message=catageory,selection=neworder.selectedorders,price=fullprice(neworder.id))

          else:

             return render_template("productselection.html",value=shownproducts,message="all",selection=neworder.selectedorders,price=fullprice(neworder.id))


@order.route("/cart",methods=["POST","GET"])
def cart():
    order=db.session.query(orders).filter_by(id=session["order"]).first()
    if request.method=="POST":
        code=request.form["coupon"]
        if request.form.get("check"):
            if not validcoupon(code,order.id) :
                return render_template("cart.html",order=order,value=order.selectedorders,message="coupon code is not valid")
            else:
                coupon=coupons.query.filter_by(managers_id=order.managerid, code=code).first()
                order.discount=coupon.discount
                db.session.commit()
                return render_template("cart.html",order=order,value=order.selectedorders,message="coupon code is valid")
        if request.form.get("checkout"):
            return redirect(url_for('order.finish'))
    else:
        return render_template("cart.html",order=order,value=order.selectedorders)
@order.route("/finish",methods=["POST","GET"])
def finish():
    order=db.session.query(orders).filter_by(id=session["order"]).first()
    manager=managers.query.filter_by(id=order.managerid).first()
    if request.method=="POST":
       order.name=request.form["name"]
       if request.form["tip"] != "":
           order.tipamount=request.form["tip"]
       db.session.commit()
       return redirect(url_for("order.qrcode"))



    else:
        return render_template("finish.html")


@order.route("/qrcode",methods=["POST","GET"])
def qrcode():
        order=db.session.query(orders).filter_by(id=session["order"]).first()
        manager=db.session.query(managers).filter_by(id=order.managerid).first()
        worker=db.session.query(workers).filter_by(id=order.workerid).first()
        price=0
        if order.discount*2<order.fullprice:
            price=order.fullprice-order.discount

        price=price+order.tipamount
        c=""
        for i in order.selectedorders:
            if c!="":
                c=c+"."

            c=c+str(i.productid)+"_"+str(i.quantity)
        c+=order.name
        d="bitcoin:"+manager.bitcoinadress+"?amount="+str(price)+"&message="+c
        if request.method=="POST":
            order.time=datetime.strptime(str(datetime.now().replace(microsecond = 0)), "%Y-%m-%d %H:%M:%S")
            db.session.commit()
            return redirect(url_for('order.finished'))
        else:
            return render_template("qrpayment.html",see=d)


@order.route("/finished",methods=["POST","GET"])
def finished():
    order=db.session.query(orders).filter_by(id=session["order"]).first()
    manager=db.session.query(managers).filter_by(id=order.managerid).first()
    if request.method=="POST":
        rating=request.form['rate']
        if int(rating)==1:
                manager.onestar=manager.onestar+1
        if int(rating)==2:
                manager.twostar=manager.twostar+1
        if int(rating)==3:
                manager.threestar=manager.threestar+1
        if int(rating)==4:
                manager.fourstar=manager.fourstar+1
        if int(rating)==5:
                manager.fivestar=manager.fivestar+1
        db.session.commit()
        return render_template("waitoverthecounter.html",name=order.name)


    return render_template("waitoverthecounter.html",name=order.name)
