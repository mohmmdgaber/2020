from flask import Flask, redirect, url_for, render_template,request,session,flash
from werkzeug.utils import secure_filename
from manager.managerpages import managerpage
##from worker.workerpage import worker
from manager.managerpages import managers
from manager.managerpages import workers
from manager.managerpages import whatmanagers
from orders.orderpage import order
from manager.managerpages import orders
from manager.managerpages import selectedorders
from flask_qrcode import QRcode
from admin.adminpages import admin
from worker.workerpage import worker
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.register_blueprint(managerpage,url_prefix="/managerpage")
app.register_blueprint(admin,url_prefix="/admin")
app.register_blueprint(worker,url_prefix="/worker")
app.register_blueprint(order,url_prefix="/order")
app.secret_key="hello"
app.config['SQLALCHEMY_BINDS']={'workers':'sqlite:///database/workers.db',
'managers':'sqlite:///database/managers.db',
'products':'sqlite:///database/products.db',
'coupons':'sqlite:///database/coupons.db',
'orders':'sqlite:///database/orders.db',
'selectedorders':'sqlite:///database/selectedorders.db'}
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["IMAGE_UPLOADS"]='./manager/static/img/productsimages'
app.config["SQLALCHEMY_TRACK_MODIFCATION"] = False

db=SQLAlchemy(app)

QRcode(app)


@app.route('/')
def home():
  db.create_all()
  return render_template("index.html")



@app.route("/logout")
def logout():
    session.pop("admin",None)
    session.pop("manager",None)
    session.pop("worker",None)

    return render_template("index.html")





if __name__ == '__main__':

    app.run(debug=True)
