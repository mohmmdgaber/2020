from flask import Blueprint,redirect, url_for, render_template,request,session,flash,current_app
from flask_sqlalchemy import SQLAlchemy
managerpage=Blueprint('managerpage', __name__, template_folder='templates',static_folder='static')
db=SQLAlchemy()
class managers(db.Model):
        _id=db.Column("id",db.Integer,primary_key=True)
        name=db.Column(db.String(100))
        password=db.Column(db.String(100))
        coffeeshop=db.Column(db.String(100))
    ##    workers = db.relationship('workers', backref='manager', lazy=True)
        def __init__(self,name,password,coffeeshop):
                self.name=name
                self.password=password
                self.coffeeshop=coffeeshop

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
            session["manager"]=found.name
            return redirect(url_for("managerpage.coffeeshop"))
        else:
            return render_template("login.html",content="The inputs you put are not correct")

    else:
        return render_template("login.html")

@managerpage.route("/coffeeshop")
def coffeeshop():
    if "manager" in session:
        return render_template("coffeeshop.html",content=(managers.query.filter_by(name=session["manager"]).first().coffeeshop),content2=(managers.query.filter_by(name=session["manager"]).first().name))

@managerpage.route("/test")
def test():
    return render_template("add,remove worker.html")

@managerpage.route("/test1")
def test1():
    return render_template("productmanager.html")

