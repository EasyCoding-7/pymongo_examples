
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

# print("... before parsing ...")

"""
for actor in actors:
    print(actor.text)
"""

# print("... after parsing ...")

"""
# 정규 표현식으로 이름만 뽑기
for actor in actors:
    newname = re.sub("\(\w*\)", "", str(actor.text))  # '\(\w*\)' : 괄호안의( \(\) ) 어떤문자( w* ) 든 '' 삭제해 달라
    print(newname)
"""

# print("... actor info print ...")

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
"""

"""
# 배우 상세정보 추출 list, dict 관리
actors_detail_info_list = list()

for actor in actors:
    # print('http://www.cine21.com' + actor.select_one('a').attrs['href'])
    actor_url = 'http://www.cine21.com' + actor.select_one('a').attrs['href']
    response_actor = requests.get(actor_url)
    soup_actor = BeautifulSoup(response_actor.content, 'html.parser')
    actor_info = soup_actor.select_one('ul.default_info')
    actor_details = actor_info.select('li')

    actor_info_dict = dict()

    for item in actor_details:
        actor_item_filed = item.select_one('span.tit').text
        actor_value = re.sub('<span.*?>.*?</span>','',str(item))
        actor_item_value = re.sub('<.*?>','',str(actor_value))
        actor_info_dict[actor_item_filed] = actor_item_value

    actors_detail_info_list.append(actor_info_dict)

print(actors_detail_info_list)


# 배우 흥행지수 뽑기
actors = soup.select('li.people_li div.name')
hits = soup.select('ul.num_info > li > strong')
movies = soup.select('ul.mov_list')

# print(actors)
# print(hits)

for index, actor in enumerate(actors):
    # print(actor)
    # print(re.sub('\(\w*\)','',actor.text))
    actor_name = re.sub('\(\w*\)','',actor.text)
    # print(hits[index])
    # print(int(hits[index].text.replace(',', '')))
    actor_hits = int(hits[index].text.replace(',', ''))
    movie_titles = movies[index].select('li a span')
    movie_titles_list = list()
    for movie in movie_titles:
        # print(movie.text)
        movie_titles_list.append(movie.text)
    print(movie_titles_list)
"""

# 배우 상세정보 추출 list, dict 관리
actors_detail_info_list = list()

# 배우 흥행지수 뽑기
actors = soup.select('li.people_li div.name')
hits = soup.select('ul.num_info > li > strong')
movies = soup.select('ul.mov_list')

for index, actor in enumerate(actors):
    # 배우이름(actor_name), hit점수(actor_hits), 대표작 리스트(movie_titles_list) 파싱
    actor_name = re.sub('\(\w*\)','',actor.text)
    actor_hits = int(hits[index].text.replace(',', ''))
    movie_titles = movies[index].select('li a span')
    movie_titles_list = list()
    for movie in movie_titles:
        movie_titles_list.append(movie.text)

    # 배우 상세정보(actor_url)
    actor_url = 'http://www.cine21.com' + actor.select_one('a').attrs['href']
    response_actor = requests.get(actor_url)
    soup_actor = BeautifulSoup(response_actor.content, 'html.parser')
    actor_info = soup_actor.select_one('ul.default_info')
    actor_details = actor_info.select('li')

    actor_info_dict = dict()
    actor_info_dict['배우이름'] = actor_name
    actor_info_dict['hits'] = actor_hits
    actor_info_dict['출연작'] = movie_titles_list

    for item in actor_details:
        actor_item_filed = item.select_one('span.tit').text
        actor_value = re.sub('<span.*?>.*?</span>','',str(item))
        actor_item_value = re.sub('<.*?>','',str(actor_value))
        actor_info_dict[actor_item_filed] = actor_item_value

    actors_detail_info_list.append(actor_info_dict)

print(actors_detail_info_list)