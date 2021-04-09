from flask import Flask
from flask_mail import Message,Mail
from datetime import date,timedelta
import pymongo
from bson import json_util
import json
from privacy import mongoConnString,myMail,emailPassword

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = myMail
app.config['MAIL_PASSWORD'] = emailPassword
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

url = mongoConnString
client = pymongo.MongoClient(url)
Database = client.get_database('notify')
if Database : 
    print("!!database connected!!")

TaskTable = Database.TaskTable

def sendEmail(recievers,message):
    msg = Message(
        'Notify',
        sender= myMail,
        recipients=[recievers]
    )
    msg.body = message+' due tommorrow!!'
    mail.send(msg)

@app.route('/')
def email():
    today = date.today()
    tomorrow = today + timedelta(1)
    query = TaskTable.find({"Date" : str(tomorrow)})
    obj = json.loads(json_util.dumps(query))
    taskArray = []
    for i in obj : 
        if(i['IsSent'] == False) :
            sendEmail(i['Email'],i['Task'])
            filter = {'Task' : i['Task']}
            newValues = {"$set" : {'IsSent' : True}}
            TaskTable.update_one(filter,newValues)
    return "sent"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4200,debug=True)