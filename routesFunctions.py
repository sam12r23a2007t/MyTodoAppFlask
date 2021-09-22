from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    descr = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

with open('config.json', 'r') as a:
    params = json.load(a)['params']

@app.route("/", methods=['POST', 'GET'])
def index():
    todo = Todo.query.filter_by().all()
    last = math.ceil(len(todo)/params['no_of_todo'])
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1

    page = int(page)
    tododata = todo[(page-1)*params['no_of_todo']:(page-1)*params['no_of_todo']+params['no_of_todo']]
    if (page==1):
        prev = "#"
        nextnum = "/?page="+str(page+1)
    elif (page==last):
        prev = "/?page="+str(page-1)
        nextnum = "#"
    else:
        prev = "/?page="+str(page-1)
        nextnum = "/?page="+str(page+1)
    return render_template('index.html', params=params, tododata=tododata, prev=prev, nextnum=nextnum, page=page)

@app.route("/operation/<string:sno>", methods=['POST', 'GET'])
def operation(sno):
    if request.method=="POST":
        title = request.form.get('title')
        descr = request.form.get('descr')
        if (sno=="0"):
            todoadd = Todo(title=title, descr=descr)
            db.session.add(todoadd)
            db.session.commit()
            return redirect('/')
        else:
            post = Todo.query.filter_by(sno=sno).first()
            post.title = title
            post.descr=descr
            db.session.commit()
            return redirect('/')
        return render_template("index.html", params=params)
    posts = Todo.query.filter_by(sno=sno).first()
    return render_template('edit.html', params=params, sno=sno, posts=posts)

@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
    deletetodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(deletetodo)
    db.session.commit()
    return redirect('/')

@app.route("/todo/<string:sno>", methods=['GET', 'POST'])
def viewtodo(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('getTodo.html', params=params, todo=todo)

@app.route("/about")
def about():
    return render_template('about.html', params=params)

if __name__=='__main__':
    app.run(debug=True)