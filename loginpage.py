from flask import Flask, redirect, url_for, render_template,request
import pylightxl as xl
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")
@app.route("/login",methods=["POST","GET"])
def login():
    db = xl.readxl(fn='Mangers.xlsx')
    a = (db.ws(ws='Sheet1').col(col=1))
    del a[0]
    b = (db.ws(ws='Sheet1').col(col=2))
    del b[0]
    c = (db.ws(ws='Sheet1').col(col=3))
    del c[0]

    if request.method=="POST":
        userr=request.form["uname"]
        password=request.form["psw"]
        z=False

        for x in range(0, len(a)):
            if str(a[x]) == userr and str(b[x]) == password:
                z = True
                coffeeshop=c[x]
        if z:
            return redirect(url_for("coffeeshop",coffeeeeshop=coffeeshop))
            ##return render_template("login.html", content="The inputs you put Right")
        else:
            return render_template("login.html",content="The inputs you put are not correct")

    else:
        return render_template("login.html")

@app.route("/<coffeeeeshop>")
def coffeeshop(coffeeeeshop):
    return render_template("coffeeshop.html",content=coffeeeeshop)


if __name__ == '__main__':
    app.run()
