from pymongo import MongoClient
from time import sleep

mongo = MongoClient()
db = mongo.mongolog.log

total = db.find().count()
cursor = db.find(tailable=True).skip(total)
while cursor.alive:
    try:
        doc = next(cursor)
        print(doc)
    except StopIteration:
        sleep(1)
