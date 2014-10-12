from flask import Flask, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
import humanize

app = Flask(__name__)
app.debug = True
mongo = MongoClient()
db = mongo.mongolog.log


@app.template_filter()
def naturaltime(datetime):
    locale_name = 'ru_RU'
    humanize.activate(locale_name)
    return humanize.naturaltime(datetime)


@app.route('/')
def index():
    logs = db.find().sort('$natural', -1).limit(10)
    return render_template('list.html', logs=logs, title='mongol')


@app.route('/event/<id>')
def event(id):
    log = db.find_one({'_id': ObjectId(id)})
    return render_template('detail.html', log=log)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
