from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import os,urllib,sys
#import models.algorithms


app= Flask(__name__)
app.config['DEBUG'] = True

#conDEBUG = 'DRIVER={ODBC Driver 17 for SQL Server};'+'Database={dbname};SERVER={dbhost};UID={dbuser};PWD={dbpass}'.format(
# conDEBUG = 'DRIVER={SQL Server};'+'DATABASE={dbname},SERVER={dbhost};PORT=1443;UID={dbuser};PWD={dbpass}'.format(
    
#     dbname=os.environ['DBNAME'],
#     dbhost=os.environ['DBHOST'],
#     dbuser=os.environ['DBUSER'],
#     dbpass=os.environ['DBPASS'],
# )

server = 'krishansqlserver.database.windows.net'
database = 'baseline'
username = 'krkusuk'
password = 'College@2019'
conDEBUG = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password

print(conDEBUG)
#conDEBUG = "DRIVER={SQL Server};Database=test;SERVER=krkusuk-pc;UID=sa;PWD=krishan_123"
conDEBUG = urllib.parse.quote_plus(conDEBUG)
conDEBUG = "mssql+pyodbc:///?odbc_connect=%s" % conDEBUG

app.config['SQLALCHEMY_DATABASE_URI'] = conDEBUG


db = SQLAlchemy(app)

@app.route("/version")
def version():
    return sys.version

    
@app.route("/heartbeat")
def heartbeat():
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
    
