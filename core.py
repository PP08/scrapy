import pymongo
from pymongo import MongoClient
import os

client = MongoClient()

db = client.testcase
table = db.test

for t in table.find():
    print(t)