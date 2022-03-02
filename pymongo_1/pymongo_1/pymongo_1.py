
import configparser
import pymongo

# read aws ip and port info
iniFile = 'aws_address.ini'
ini_parser = configparser.ConfigParser()
ini_parser.read(iniFile)

# connection db
connection = pymongo.MongoClient(str(ini_parser['aws']['ip']), int(ini_parser['aws']['port']))
db_test1 = connection.test1
# print(db)
# print(db.name)

# create or connect collection
test_collection = db_test1.test_collection
# print(test_collection)

# test INSERT
post = {"user":"user01", "guild":"superman", "type":"knight", "tags":["newbe", "hell"]}
test_collection.insert_one(post)

# FIND
find_result = test_collection.find_one({"user":"user01"})
# print(find_result)

# UPDATE
test_collection.update_one( {
        "user":"user01",
        {
            "$set" : {"test":"update test"}
        }
    }
)