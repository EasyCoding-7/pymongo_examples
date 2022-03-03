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

# 테스트를 위해 처음은 INDEX 삭제해 준다.
actor_collection.drop_indexes()

# compound indexing
actor_collection.create_index(
    [
        ('출연작', pymongo.TEXT),
        ('직업', pymongo.TEXT),
        ('hits', pymongo.TEXT)
    ]
)

# 검색해 보자면
docs = actor_collection.find(
    {
        '$text' : 
        {
            '$search' : '가수'
        }
    }
)
for doc in docs:
    print(doc)