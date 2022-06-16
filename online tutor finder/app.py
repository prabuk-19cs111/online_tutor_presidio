from flask import Flask, render_template,request,redirect,url_for,flash,session
from flask_login import login_required
from functools import wraps
from pymongo import MongoClient
import hashlib
import json
app = Flask(__name__)
app.secret_key  = "unauthorized0"
session={}
session['log_status']=None

def login_check(uname,pword):
   
    for i in ttr.find():
        if uname == i["name"] and pword == i["pass"]:
            session['log_status']=True
            return True


def student_login_check(uname,pword):
    for i in stu.find():
        if uname == i["name"] and pword == i["pass"]:
            session['log_status']=True
            return True


def event_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['event_name']==None:
            flash("Please select an event","Error")
            return redirect(url_for('edit'))
        else:
            return f(*args, **kwargs)

    return decorated_function

def login_required(f):
   @wraps(f)
   def wrap(*args,**kwargs):
      if session['log_status']:
            return f(*args,**kwargs)
      else:
            flash("please login","Error")
            return redirect(url_for('login'))
   return wrap

@app.route('/login',methods=('GET','POST'))
def login():
   keys = ["username","password"]
   d = dict.fromkeys(keys,None)
   if request.method == 'POST':
      d["username"] = request.form.get("uname")
      d["password"] = request.form.get("pword")
      if login_check(d["username"],d["password"]):
         session['username']=d["username"]
         session['password']=d["password"]
         flash("Login Successful","success")
         return redirect(url_for('create'))
      else:
         flash("Login Credentials Doesnot match","Error")
         return redirect(url_for('login'))
   return render_template('login.html')

@app.route('/passwordchange/',methods=('GET','POST'))
@login_required
def changepword():
   if request.method=='POST':
      cu =request.form['curr_pass']
      m1 = request.form['match1']
      m2 = request.form['match2']
      i = cred.find({"username":session['username']})
      for c in i:
             pass
      x=c['password']
      if x==hashlib.sha512(cu.encode()).hexdigest():
            if m1==m2:
                  cred.delete_one({"password":x})
                  c['password']=hashlib.sha512(m1.encode()).hexdigest()
                  cred.insert_one(c)
                  flash("Password changed Successfully","success")
                  return redirect(url_for('home'))
            else:
               flash("Password doesnot match","Error")
               return redirect(url_for('changepword'))
      else:
             flash("Incorrect password","Error")
             return redirect(url_for('changepword'))
   return render_template('passwordchange.html')

   

@app.route('/delete/',methods=('GET','POST'))
@login_required
def delete():
   a = ttr.find({"name":session["username"]})
   d={}
   for i in a:
      d = i
   if request.method=='POST':
      del_ename = request.form['venue']
      if del_ename!="none":
         d['subject'].remove(del_ename)
         ttr.delete_one({"name":session["username"]})
         ttr.insert_one(d)
         return redirect(url_for('create'))
      else:
         flash("Select an event to delete","Error")
         return redirect(url_for('delete'))
   return render_template('delete.html',l=d['subject'])

@app.route('/logout/')
@login_required
def logout():
       session['log_status']=None
       session['username']=None
       session['password']=None
       flash("Logged Out Successfully","success")
       return redirect(url_for('login'))


@app.route('/create/',methods=('GET','POST'))
@login_required
def create():
   keys = ["cname","ename","date","desc","time","venue","link"]
   inserted_doc  = dict.fromkeys(keys,None)
   if request.method == 'POST':
      inserted_doc['venue'] = request.form['venue']
      a = ttr.find({"name":session["username"]})
      d={}
      for i in a:
             d = i
      d['subject'].insert(-1,inserted_doc['venue'])
      ttr.delete_one({"name":session["username"]})
      ttr.insert_one(d)
      flash("Created Successfully","success")
      return "<h1>Done</h1>"
   return render_template('create.html')


@app.route("/feed")
def index():
   return render_template("index.html",l=ttr.find())
   
@app.route("/studentlogin",methods = ('GET','POST'))
def studentlogin():
   keys = ["username","password"]
   d = dict.fromkeys(keys,None)
   if request.method == 'POST':
      d["username"] = request.form.get("uname")
      d["password"] = request.form.get("pword")
      if student_login_check(d["username"],d["password"]):
         return redirect(url_for('index'))
      else:
         flash("Login Credentials Doesnot match","Error")
         return redirect(url_for('studentlogin'))
   return render_template("loginstudent.html")

@app.route("/")
def home():
   return render_template("home.html")

if __name__ == '__main__':
  # client = MongoClient("mongodb://admin:MNUERTvp7d0LNoCP@SG-H2KSP-48981.servers.mongodirector.com:27017/admin")
   client = MongoClient("mongodb://localhost:27017")
   db = client['events']
   db1 = client['tutor']
   ttr = db1['tutors']
   stu = db1['students']
   col = db['posts']
   cred  = db['users']
   app.run(debug=True)