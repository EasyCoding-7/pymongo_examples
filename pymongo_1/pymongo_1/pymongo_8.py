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

# INDEX 생성
actor_collection.create_index('배우이름')
#print(actor_collection.index_information())

# INDEX 삭제
actor_collection.drop_indexes()

"""
# text로 indexing이 되어있지 않기에 아래서 에러 리턴
docs = actor_collection.find( 
    {
        '$text' : 
        {
            '$search' : '범죄' 
        } 
    } 
)
for doc in docs:
    print(doc)
"""

# text index를 지정해보자.
actor_collection.create_index( [ ('출연작', 'text') ] )

# 재시도
docs = actor_collection.find( 
    {
        '$text' : 
        {
            '$search' : '왕' 
        } 
    } 
)
for doc in docs:
    print(doc)