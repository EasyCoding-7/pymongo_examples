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

# column 수정
actor_collection.update_many({}, {'$rename': {'다른 이름':'새로운이름'}} )

# 하나출력
print(actor_collection.find_one({}))

# 갯수지정해 출력
docs = actor_collection.find({}).limit(3)
for doc in docs:
    print(doc)

# 정렬
docs = actor_collection.find({}).sort('생년월일', pymongo.DESCENDING).limit(20)
for doc in docs:
    print(doc)

# 특정필드 확인
docs = actor_collection.find( {'특기': {'$exists': True}} ).sort('흥행지수').limit(5)
for doc in docs:
    print(doc)

docs = actor_collection.find( {'생년월일': {'$exists': False}}, {'배우이름':1, '_id':1} )
for doc in docs:
    print(doc)