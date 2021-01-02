from flask import Blueprint,redirect, url_for, render_template,request,session,flash,current_app
from flask_sqlalchemy import SQLAlchemy
from manager.managerpages import managers
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
           found=managers.query.filter_by(name=managerdataname).first()
           if found:
                 found.coffeeshop=managerdatacoffee
                 found.password=managerdatapassword
                 db.session.commit()
                 return render_template("adminmanagementpage.html",value=managers.query.all())
           else:
                    mnager=managers(managerdataname,managerdatapassword,managerdatacoffee)
                    db.session.add(mnager)
                    db.session.commit()
                    return render_template("adminmanagementpage.html",value=managers.query.all())
        elif request.form.get("remove"):
             removename=request.form["deleteuser"]
             managers.query.filter_by(name=removename).delete()
             db.session.commit()
             return render_template("adminmanagementpage.html",value=managers.query.all())

        else:
             return render_template("adminmanagementpage.html",value=managers.query.all())

    else:
      if "admin" in session:
          return render_template("adminmanagementpage.html",value=managers.query.all())
      else:
          return redirect(url_for('/'))
