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
# nor
docs = actor_collection.find( 
    { 
        '$nor' : 
        [ 
            { 'hits' : { '$gte': 10000 } }, 
            { 'hits' : { '$lt': 1000 } } 
        ] 
    }, 
    { '배우이름':1, '_id':0 } 
)
for doc in docs:
    print(doc)
"""

# in
docs = actor_collection.find( 
    { 
        'hits' : 
        {
            '$nin': [9182]
        }
    }, 
    { '배우이름':1, '_id':0 } 
)
for doc in docs:
    print(doc)