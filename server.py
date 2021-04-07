from flask import Flask
from flask_mail import Message,Mail

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ironman2640@gmail.com'
app.config['MAIL_PASSWORD'] = 'ironman@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def sendEmail(recievers,message):
    msg = Message(
        'Task Notification',
        sender='ironman2640@gmail.com',
        recipients=[recievers]
    )
    msg.body = message+'due tommorrow!!'
    mail.send(msg)


if __name__ == '__main__':
    app.run(debug=True)