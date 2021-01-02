from flask import Flask, redirect, url_for, render_template,request,session,flash
from manager.managerpages import managerpage
from manager.managerpages import managers
from admin.adminpages import admin
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.register_blueprint(managerpage,url_prefix="/managerpage")
app.register_blueprint(admin,url_prefix="/admin")
app.secret_key="hello"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database/managers.db'
app.config["SQLALCHEMY_TRACK_MODIFCATION"] = False
db=SQLAlchemy(app)

##class managers(db.Model):
##    _id=db.Column("id",db.Integer,primary_key=True)
##    name=db.Column(db.String(100))
##    password=db.Column(db.String(100))
##    coffeeshop=db.Column(db.String(100))
##    workers = db.relationship('workers', backref='manager', lazy=True)
##    def __init__(self,name,password,coffeeshop):
##            self.name=name
##            self.password=password
##            self.coffeeshop=coffeeshop

##class workers(db.Model):
##    _id=db.Column("id",db.Integer,primary_key=True)
##    name=db.Column(db.String(100))
    ##password=db.Column(db.String(100))
    ##coffeeshop=db.Column(db.String(100))
    ##manager_id=db.Column(db.Integer,db.Foreign_Key('workers.id'))





@app.route('/')
def home():
  db.create_all()
  return render_template("index.html")



@app.route("/logout")
def logout():
    session.pop("admin",None)
    session.pop("manager",None)
    return render_template("index.html")





if __name__ == '__main__':

    app.run(debug=True)
