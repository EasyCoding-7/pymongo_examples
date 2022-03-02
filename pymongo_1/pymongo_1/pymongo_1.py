
import configparser
import pymongo

# read aws ip and port info
iniFile = 'aws_address.ini'
ini_parser = configparser.ConfigParser()
ini_parser.read(iniFile)

# connection db
connection = pymongo.MongoClient(str(ini_parser['aws']['ip']), int(ini_parser['aws']['port']))
db = connection.users
print(db)