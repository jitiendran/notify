from flask import Flask
from flask.templating import render_template
app = Flask(__name__,template_folder='main')

@app.route('/')
def index() :
    return render_template('index.html',style='./static/styles/style.css',icon='./static/images/icon.png')

if __name__ == '__main__' :
    app.run(debug=True) 