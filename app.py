from os import name
from flask import Flask,request,redirect
from flask.helpers import url_for
from flask.templating import render_template
from datetime import date
import pymongo
from bson import json_util
import json

from pymongo import database

url = 'mongodb+srv://jiji:123@cluster0.md3ui.mongodb.net/test'
logged = False
app = Flask(__name__,template_folder='main')
client = pymongo.MongoClient(url)
Username = 'name'
Database = client.get_database('notify')
if Database : 
    print("!!database connected!!")

SampleTable = Database.SampleTable
TaskTable = Database.TaskTable
UserTable = Database['name']

@app.route('/')
def index() :
    return render_template('index.html',style='./static/styles/style.css',icon='./static/images/icon.png')


@app.route('/signup')
def register():
    return render_template('register.html',style='./static/styles/style.css',icon='./static/images/icon.png')


@app.route('/register',methods=['POST'])
def signup():
    queryObject = {
        'Username' : request.form['Username'],
        'Password' : request.form['Password']
    }
    #creating a collection on username for storing tasks
    query = SampleTable.insert_one(queryObject)
    print(request.form['Username'])
    return redirect(url_for('User',name = request.form['Username']))


@app.route('/login',methods=['POST'])
def login() : 
    queryObj = {"Username" : request.form['Username']}
    query = SampleTable.find_one(queryObj)
    obj = json.loads(json_util.dumps(query))
    return redirect(url_for('User',name = obj['Username']))

# print('This is the object : ',obj)
# Username = obj['Username']


@app.route('/tasks',methods=['POST'])
def createTasks():
    queryObject = {
        'Task' : request.form['Task'],
        'Date' : request.form['Date']
    }
    query = UserTable.insert_one(queryObject)
    return redirect(url_for('User',name=Username))

@app.route('/User',methods=['GET'])
def User() :
    today = date.today()
    user = request.args.get('name')
    global Username
    Username = user
    global UserTable
    UserTable = Database[user]
    # print(Username)
    query = UserTable.find({"Date": str(today)})
    obj = json.loads(json_util.dumps(query))
    task = []
    # k = 0
    for i in obj : 
        task.append(str(i['Task']))
        
    return render_template('user.html',name = user,progress = 10,tasks = task)

@app.route('/Delete',methods=['GET'])
def delete():
    task = request.args.get('task')
    query = UserTable.delete_one({"Task": task})
    print('Hello this is delete')
    return redirect(url_for('User',name=Username))

    

if __name__ == '__main__' :
    app.run(debug=True) 