import configparser
import pymongo

# read aws ip and port info
iniFile = 'aws_address.ini'
ini_parser = configparser.ConfigParser()
ini_parser.read(iniFile)

# connection db, collection
conn = pymongo.MongoClient(str(ini_parser['aws']['ip']), int(ini_parser['aws']['port']))
actor_db = conn.cine21_actor
actor_collection = actor_db.actor_collection

"""
docs = actor_collection.find( {'hits': {'$gte': 10000}})
for doc in docs:
    print(doc)
"""

"""
# or 연산
docs = actor_collection.find( {'$or': [{'출연작':'극한직업'}, {'출연작':'더 킹'}]}, {'배우이름':1, '_id':0})
for doc in docs:
    print(doc)
"""

# or 연산2
docs = actor_collection.find( { 'hits': { '$gte':100 },  '$or' : [ {'출연작':'극한직업'}, {'출연작':'더 킹'} ] }, { '배우이름':1, '_id':0 } )
for doc in docs:
    print(doc)