from flask import Blueprint,redirect, url_for, render_template,request,session,flash,current_app
from flask_sqlalchemy import SQLAlchemy
from manager.managerpages import managers
from manager.managerpages import workers
from manager.managerpages import productss
from manager.managerpages import coupons
from manager.managerpages import whatmanagers

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

import os


admin=Blueprint('admin', __name__, template_folder='templates',static_folder='static')
db=SQLAlchemy()
@admin.route("/",methods=["POST","GET"])
def home():
    db.create_all()
    if "admin" in session:
           return redirect(url_for("admin.management"))
    if request.method=="POST":
       password=request.form["psw"]
       if(password=="1234"):
           session["admin"]=password
           return redirect(url_for('admin.management'))
       else:
           return render_template("adminsterpage.html",content="The input is not correct")

    else:
     return render_template("adminsterpage.html")

@admin.route("/management",methods=["POST","GET"])
def management():
    if request.method=="POST":
        if  request.form.get("add"):
           managerdataname=request.form["managername"]
           managerdatapassword=request.form["managerpassword"]
           managerdatacoffee=request.form["managercoffee"]
           bitcoinaddress=request.form["bitcoinaddress"]
           found=managers.query.filter_by(name=managerdataname).first()
           if found:
                 found.coffeeshop=managerdatacoffee
                 found.password=managerdatapassword
                 found.bitcoinaddress=managerdatapassword

                 db.session.commit()
                 return render_template("adminmanagementpage.html",value=managers.query.all())
           else:
                    mnager=managers(name=managerdataname,password=managerdatapassword,coffeeshop=managerdatacoffee,sales=0,revenue=0,startday=0,starthour=0,endday=0,endhour=0,lateststate="This is a new coffeeshop!!!!",isthestoreopen=False,bitcoinadress=bitcoinaddress,onestar=0,twostar=0,threestar=0,fourstar=0,fivestar=0)
                    db.session.add(mnager)
                    db.session.commit()
                    return render_template("adminmanagementpage.html",value=managers.query.all())
        elif request.form.get("remove"):
             removename=request.form["deleteuser"]
             found=managers.query.filter_by(name=removename).first()
             workers.query.filter_by(managers_id=found.id)
             coupons.query.filter_by(managers_id=found.id)
             for item in found.products:
                 os.remove(os.path.join(current_app.config["IMAGE_UPLOADS"], item.imagename))
                 db.session.delete(item)
             managers.query.filter_by(name=removename).delete()
             db.session.commit()
             return render_template("adminmanagementpage.html",value=managers.query.all())

        else:
             return render_template("adminmanagementpage.html",value=managers.query.all())

    else:
      if "admin" in session:
          whatmanagers()
          return render_template("adminmanagementpage.html",value=managers.query.all())
      else:
          return redirect(url_for('/'))
