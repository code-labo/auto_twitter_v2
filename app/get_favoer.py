"""
自分のツイートにいいねした人をfavoerとしてDBにpush
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import numpy as np
import psycopg2
import random

from src.auto_twitter import AutoTwitter
from src.envs import *
from src.filters import date_filter

def main():
    tweet_num=GET_FAVOER_CFG["TWEET_NUM"] #取得するツイートの数
    account_num_max=GET_FAVOER_CFG["ACCOUNT_NUM_MAX"]

    ##既に登録済みのメンバー(favoerとfollowed)を取得
    conn=psycopg2.connect(
        host=HOST,user=USER,password=PASSWORD,database=DATABASE
    )
    with conn:
        with conn.cursor() as cursor:
            query="""SELECT id,name FROM account 
                     WHERE roll='favoer' OR roll='followed';"""
            cursor.execute(query)
            result=np.array(cursor.fetchall())

            if not len(result)==0:
                member_name_db=[name.replace(" ","") for name in result[:,1].flatten()]
            else:
                member_name_db=[]

            #最大idの取得.自動で振り分けされない.なんでや
            query="SELECT MAX(id) FROM account;"
            cursor.execute(query)
            result=cursor.fetchone()
            id_last=int(result[0]) if not result[0] is None else 0
            #

        conn.commit()
    ##

    base_url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(f"{base_url}/{ACCOUNT_NAME}")

    ##今の画面のツイートをtweet_num件取得
    tweets=[]
    current_height=0
    while len(tweets)<tweet_num:

        tweets+=auto_twitter.get_tweet(
            filters=[date_filter]
        ) #ツイートの取得

        current_height+=auto_twitter.scroll_page(current_height) #ページをスクロール

    tweets=np.array(tweets)
    ##

    ##取得したツイートにいいねした人を取得
    favoers_name=[]
    for tweet in tweets[:,0]:
        
        favoers_link_tmp=auto_twitter.get_favoers(tweet_url=tweet)

        #既にデータベースに入ってるやつははじく
        for favoer_link in favoers_link_tmp:
            favoer_name=favoer_link.replace("https://twitter.com/","")
            if not favoer_name in member_name_db and not favoer_name in favoers_name:
                favoers_name.append(favoer_name)
        #
    ##

    account_num_max=account_num_max if len(favoers_name)>account_num_max else len(favoers_name)
    favoers_name=random.sample(favoers_name,account_num_max)

    # print(range(id_last+1,id_last+len(favoers_name)+1))
    # print(favoers_name)
    favoers=[
        [id,name]
        for id,name
        in zip(range(id_last+1,id_last+len(favoers_name)+1),favoers_name)
    ]

    print("***Favoers***")
    print(np.array(favoers))

    #DBに登録
    with conn:
        with conn.cursor() as cursor:
            query="""INSERT INTO account
                     (id,name,roll)
                     VALUES(%s,%s,'favoer');"""
            cursor.executemany(query,favoers)
        conn.commit()


if __name__=="__main__":
    main()