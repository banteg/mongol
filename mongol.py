from flask import Flask, render_template, Response, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import humanize
from time import sleep
import json

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


def firehose():
    total = db.find().count()
    cursor = db.find(tailable=True).skip(total)
    while cursor.alive:
        try:
            doc = next(cursor)
            dump = json.dumps(doc, default=json_util.default)
            yield 'data: {}\n\n'.format(dump)
        except StopIteration:
            sleep(1)


@app.route('/api/stream')
def stream():
    return Response(firehose(),
                    mimetype='text/event-stream')


@app.route('/api/last/<int:count>')
def last(count):
    log = db.find().sort('$natural', -1).limit(count)
    data = {'data': list(log)}
    return Response(json_util.dumps(data),
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, threaded=True)
