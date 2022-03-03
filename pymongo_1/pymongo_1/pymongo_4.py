
import configparser
import pymongo
import requests
from bs4 import BeautifulSoup
import re                       # regular expression

# 배우 상세정보 추출 list, dict 관리
actors_detail_info_list = list()

# read aws ip and port info
iniFile = 'aws_address.ini'
ini_parser = configparser.ConfigParser()
ini_parser.read(iniFile)

# connection db, collection
conn = pymongo.MongoClient(str(ini_parser['aws']['ip']), int(ini_parser['aws']['port']))
actor_db = conn.cine21_actor
actor_collection = actor_db.actor_collection
actor_collection.delete_many({})

# crawlling
url = "http://www.cine21.com/rank/person/content"
post_data = dict()
post_data['section'] = 'actor'
post_data['period_start'] = '2020-03'
post_data['gender'] = 'all'

for pindex in range(1, 21):
    post_data['page'] = pindex

    res = requests.post(url, data=post_data)

    # parsing
    soup = BeautifulSoup(res.content, 'html.parser')
    actors = soup.select('li.people_li div.name')

    # 배우 흥행지수 뽑기
    actors = soup.select('li.people_li div.name')
    hits = soup.select('ul.num_info > li > strong')
    movies = soup.select('ul.mov_list')
    rankings = soup.select('li.people_li > span.grade')

    for index, actor in enumerate(actors):
        # 배우이름(actor_name), hit점수(actor_hits), 대표작 리스트(movie_titles_list) 파싱
        actor_name = re.sub('\(\w*\)','',actor.text)
        actor_hits = int(hits[index].text.replace(',', ''))
        actor_rank = int(rankings[index].text)
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
        actor_info_dict['rank'] = actor_rank
        actor_info_dict['출연작'] = movie_titles_list

        for item in actor_details:
            actor_item_filed = item.select_one('span.tit').text
            actor_value = re.sub('<span.*?>.*?</span>','',str(item))
            actor_item_value = re.sub('<.*?>','',str(actor_value))
            actor_info_dict[actor_item_filed] = actor_item_value

        actors_detail_info_list.append(actor_info_dict)

# print(actors_detail_info_list)
actor_collection.insert_many(actors_detail_info_list)