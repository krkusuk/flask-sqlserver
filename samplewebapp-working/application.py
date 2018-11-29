from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import urllib

app= Flask(__name__)

conDEBUG = "DRIVER={SQL Server};Database=test;SERVER=krkusuk-pc;UID=sa;PWD=krishan_123"
conDEBUG = urllib.parse.quote_plus(conDEBUG)
conDEBUG = "mssql+pyodbc:///?odbc_connect=%s" % conDEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = conDEBUG


#conDEBUG = "DRIVER={SQL Server};Database=test;SERVER=qabdepdv5e.database.windows.net;UID=agorappesa;PWD=201501Im@gination"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql://sa:krishan_123@localhost/test'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)




@app.route("/hello")
def hello():
    return 'Hello World!'


@app.route('/addnewpost', methods=['GET'])
def view_registration_form():
    return render_template('postadd.html')


@app.route('/addnewpost', methods=['POST'])
def register_post():
    from model import Post
    title = request.form.get('title')
    body = request.form.get('body')
    categoryid = request.form.get('categoryid')

    post = Post(title=title, body=body,category_id=categoryid)
    db.session.add(post)
    db.session.commit()
    return 'done'

@app.route('/', methods=['GET'])
def list_all():
    from model import Post
    posts = Post.query.all()
    
    return render_template('showposts.html',posts=posts)



