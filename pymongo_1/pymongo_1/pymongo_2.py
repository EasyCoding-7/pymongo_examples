
import configparser
import pymongo
import requests
from bs4 import BeautifulSoup
import re                       # regular expression

# read aws ip and port info
iniFile = 'aws_address.ini'
ini_parser = configparser.ConfigParser()
ini_parser.read(iniFile)

# connection db, collection
conn = pymongo.MongoClient(str(ini_parser['aws']['ip']), int(ini_parser['aws']['port']))
actor_db = conn.cine21_actor
actor_collection = actor_db.actor_collection

# crawlling
url = "http://www.cine21.com/rank/person/content"
post_data = dict()
post_data['section'] = 'actor'
post_data['period_start'] = '2020-03'
post_data['gender'] = 'all'
post_data['page'] = 1

res = requests.post(url, data=post_data)

# parsing
soup = BeautifulSoup(res.content, 'html.parser')
actors = soup.select('li.people_li div.name')

print("... before parsing ...")

for actor in actors:
    print(actor.text)

print("... after parsing ...")

# 정규 표현식으로 이름만 뽑기
for actor in actors:
    newname = re.sub("\(\w*\)", "", str(actor.text))  # '\(\w*\)' : 괄호안의( \(\) ) 어떤문자( w* ) 든 '' 삭제해 달라
    print(newname)

print("... actor info print ...")

"""
# 배우 상세정보 추출(정규표현식 이용 전)
for actor in actors:
    # print('http://www.cine21.com' + actor.select_one('a').attrs['href'])
    actor_url = 'http://www.cine21.com' + actor.select_one('a').attrs['href']
    response_actor = requests.get(actor_url)
    soup_actor = BeautifulSoup(response_actor.content, 'html.parser')
    actor_info = soup_actor.select_one('ul.default_info')
    actor_details = actor_info.select('li')
    for item in actor_details:
        print(item)
"""

# 배우 상세정보 추출(정규표현식 이용)
for actor in actors:
    # print('http://www.cine21.com' + actor.select_one('a').attrs['href'])
    actor_url = 'http://www.cine21.com' + actor.select_one('a').attrs['href']
    response_actor = requests.get(actor_url)
    soup_actor = BeautifulSoup(response_actor.content, 'html.parser')
    actor_info = soup_actor.select_one('ul.default_info')
    actor_details = actor_info.select('li')
    for item in actor_details:
        # print(item)
        print(item.select_one('span.tit').text)
        actor_value = re.sub('<span.*?>.*?</span>','',str(item))
        print(re.sub('<.*?>','',str(actor_value)))