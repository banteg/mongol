from flask import Flask, render_template, abort
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True
mongo = MongoClient()
db = mongo.mongolog.log


@app.route('/')
def index():
    logs = db.find().sort('$natural', -1).limit(10)
    return render_template('index.html', logs=logs, title='mongol')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
