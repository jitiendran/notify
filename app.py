from os import name
from flask import Flask,request,redirect
from flask.helpers import url_for
from flask.templating import render_template
from datetime import date
import pymongo
from bson import json_util
import json
url = 'mongodb+srv://jiji:123@cluster0.md3ui.mongodb.net/test'
logged = False
app = Flask(__name__,template_folder='main')
client = pymongo.MongoClient(url)
Database = client.get_database('notify')
if Database : 
    print("!!database connected!!")
SampleTable = Database.SampleTable
TaskTable = Database.TaskTable

@app.route('/')
def index() :
    return render_template('index.html',style='./static/styles/style.css',icon='./static/images/icon.png')
@app.route('/register')
def signup():
    queryObject = {
        'Username' : 'Jitiendran',
        'Email' : '',
        'Image' : '',
        'Password' : '123'
    }
    query = SampleTable.insert_one(queryObject)
    return "Data inserted !!!"

@app.route('/login',methods=['POST'])
def login() : 
    queryObj = {"Username" : request.form['Username']}
    query = SampleTable.find_one(queryObj)
    obj = json.loads(json_util.dumps(query))
    return redirect(url_for('User',name = obj['Username']))

# print('This is the object : ',obj)
# Username = obj['Username']

@app.route('/User',methods=['GET'])
def User() :
    today = date.today()
    user = request.args.get('name')
    query = TaskTable.find({"Date": str(today)})
    obj = json.loads(json_util.dumps(query))
    task = []
    # k = 0
    for i in obj : 
        task.append(str(i['Task']))
        
    return render_template('user.html',name = user,progress = 10,tasks = task)

if __name__ == '__main__' :
    app.run(debug=True) 