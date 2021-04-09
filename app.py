from flask import Flask,request,redirect
from flask.globals import session
from flask.helpers import url_for
from flask.templating import render_template
from datetime import date
import pymongo
from bson import json_util
import json

app = Flask(__name__,template_folder='main')


url = 'mongodb+srv://jiji:123@cluster0.md3ui.mongodb.net/test'
client = pymongo.MongoClient(url)
Database = client.get_database('notify')

if Database : 
    print("!!database connected!!")

UserTable = Database['UserTable']
TaskTable = Database['TaskTable']

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
        'Email' : request.form['Email'],
        'Password' : request.form['Password']
    }
    query = UserTable.insert_one(queryObject)
    print(request.form['Username'])
    return redirect(url_for('User',name = request.form['Username']))


@app.route('/login',methods=['POST'])
def login() : 
    queryObj = {"Username" : request.form['Username']}
    query = UserTable.find_one(queryObj)
    obj = json.loads(json_util.dumps(query))
    return redirect(url_for('User',name = obj['Username']))



@app.route('/tasks',methods=['POST'])
def createTasks():
    user = UserTable.find_one({"Username": session['Username']})
    obj = json.loads(json_util.dumps(user))
    queryObject = {
        'Task' : request.form['Task'],
        'Date' : request.form['Date'],
        'Email' : obj['Email'],
        'IsSent' : False
    }
    query = TaskTable.insert_one(queryObject)
    return redirect(url_for('User',name=session['Username']))


@app.route('/User',methods=['GET'])
def User() :
    today = date.today()
    user = request.args.get('name')
    session['Username'] = user
    query = TaskTable.find({"Date": str(today)})
    obj = json.loads(json_util.dumps(query))
    task = []
    for i in obj : 
        task.append(str(i['Task']))

    return render_template('user.html',name = user,progress = 10,tasks = task)


@app.route('/Delete',methods=['GET'])
def delete():
    task = request.args.get('task')
    query = TaskTable.delete_one({"Task": task})
    print('Hello this is delete')
    return redirect(url_for('User',name=session['Username']))


if __name__ == '__main__' :
    app.run(debug=True) 