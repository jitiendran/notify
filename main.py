from flask import Flask,request,jsonify
from flask.templating import render_template
import pymongo
from bson import json_util
import json
url = 'mongodb+srv://jiji:123@cluster0.md3ui.mongodb.net/test'
app = Flask(__name__,template_folder='main')
client = pymongo.MongoClient(url)
Database = client.get_database('notify')
if Database : 
    print("!!database connected!!")
SampleTable = Database.SampleTable

@app.route('/')
def index() :
    return render_template('index.html',style='./static/styles/style.css',icon='./static/images/icon.png')
@app.route('/register')
def signup():
    queryObject = {
        'Username' : 'Jitiendran',
        'Password' : '123'
    }
    query = SampleTable.insert_one(queryObject)
    return "Data inserted !!!"

@app.route('/login',methods=['POST'])
def login() : 
    queryObj = {"Username" : request.form['Username']}
    query = SampleTable.find_one(queryObj)
    return json.loads(json_util.dumps(query))

if __name__ == '__main__' :
    app.run(debug=True) 