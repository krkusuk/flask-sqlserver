from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import os,urllib
#import models.algorithms


app= Flask(__name__)

conDEBUG = 'DRIVER={SQL Server};'+'Database={dbname};SERVER={dbhost};UID={dbuser};PWD={dbpass}'.format(
    
    dbname=os.environ['DBNAME'],
    dbhost=os.environ['DBHOST'],
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
)
print(conDEBUG)
#conDEBUG = "DRIVER={SQL Server};Database=test;SERVER=krkusuk-pc;UID=sa;PWD=krishan_123"
conDEBUG = urllib.parse.quote_plus(conDEBUG)
conDEBUG = "mssql+pyodbc:///?odbc_connect=%s" % conDEBUG

app.config['SQLALCHEMY_DATABASE_URI'] = conDEBUG


db = SQLAlchemy(app)

@app.route("/heartbeat")
def index():
    return "Baseline web is alive!"

@app.route("/")
def index():
    from models.algorithms import Algorithm
    algos = Algorithm.query.all()
    return render_template('showalgos.html',algos=algos)

@app.route("/addalgo", methods=['GET'])
def addalgo():
    return render_template('addalgo.html')

@app.route("/addalgo", methods=['POST'])
def addalgo_post():
    from models.algorithms import Algorithm
    name = request.form.get('algoname')
    grain = request.form.get('grain')
    newalgo = Algorithm(name=name,grain_in_minutes=grain)
    try:
        db.session.add(newalgo)
        db.session.commit()
        return render_template('success.html')
    except:
        return render_template('failure.html',error = 'Error while adding value in db.')
    
