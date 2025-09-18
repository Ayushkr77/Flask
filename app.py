# PS C:\Users\ayush\Desktop\Flask> virtualenv env
# PS C:\Users\ayush\Desktop\Flask> .\env\Scripts\activate.ps1
# (env) PS C:\Users\ayush\Desktop\Flask> pip install flask
# Make sure u run python file inside virtual env only, otherwise error as modules installed will be present inside virtual env only
# We can also read the static files by http://127.0.0.1:5000/static/ayush.txt
# For better understanding, must see all the commits

# Base.html comments:  Commments written here, bcz if written there then there was Jinja syntax error
# {% block title %} → Placeholder for the page title (child templates can override it).
# {% block head %} → Extra content (like meta tags, custom scripts) can be inserted by child templates.
# Jinja syntax    {% block body %} → The main content area of the page. Child templates will replace this. If we write something inside it, it acts as default content. Child templates can override it (replace it) or extend it with {{ super() }}.
# base.html is like a blueprint for all pages.

# index.html comments
# {% extends 'base.html' %}   Inherits the structure from base.html. 
# {% block head %}   Currently empty, but you could add custom <script> or <style> just for this page.
# Benefit of Jinja: You don’t repeat <head>, <html>, <body>, CSS links in every page. Only write unique content in child templates.



from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ayush%401122@localhost:3306/tododb'   # we can see the databases and tables using cmd or in mysql workbench by show databases; show tables;...
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # suppress warning
db=SQLAlchemy(app)

class Todo(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    content= db.Column(db.String(200), nullable=False)
    completed= db.Column(db.Integer, default=0)
    date_created= db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r>' % self.id
    
# Create tables
with app.app_context():
    db.create_all()


@app.route("/", methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)
    

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

# @app.route("/")
# def hello_world():
#     # return "Hello World!"
#     return render_template("index.html")

# @app.route("/products")
# def products():
#     return "This is products page"

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, port=8000)    # if want to change the port