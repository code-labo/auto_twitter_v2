"""
ツイートを検索し、DBにURLを保存する
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import numpy as np
from math import floor
import psycopg2
from datetime import datetime

from src.auto_twitter import AutoTwitter
from src.filters import date_filter
from src.envs import *
from src.utils import add_single_quote


def main():

    num_account=GET_FOLLOWERS_TWEET_CFG["NUM_ACCOUNT"]
    now_datetime=datetime.now()

    base_url="https://twitter.com"
    auto_twitter=AutoTwitter(driver_name="msedgedriver.exe")
    auto_twitter.access_url(url=base_url)


    ##データベースへの接続
    conn=psycopg2.connect(
        host=HOST,user=USER,password=PASSWORD,database=DATABASE
    )

    with conn:
        with conn.cursor() as cursor:

            #最大idの取得.自動で振り分けされない.なんでや
            query="SELECT MAX(id) FROM tweet;"
            cursor.execute(query)
            result=cursor.fetchone()
            id_last=int(result[0]) if not result[0] is None else 0
            #
            
            #アカウントのurlを取得
            except_account_query="("+",".join(map(add_single_quote,EXCEPT_ACCOUNT))+")"
            query=f"""SELECT id,name 
                     FROM account
                     WHERE roll='follower'
                     AND NOT name IN {except_account_query}
                     ORDER BY favo_at ASC
                     LIMIT {num_account};"""
            print(query)
            cursor.execute(query)
            result=np.array(cursor.fetchall())

            if len(result)>0:
                account_ids=result[:,0].flatten()
                account_names=[account_name.replace(" ","") for account_name in result[:,1].flatten()]
            #
        conn.commit()
    print(result)
    if len(result)==0:
        print("***No Follower***")
        exit(1)


    #1つのアカウントにつき最新のツイートを1つ取ってくる
    idx=1
    register_values=[] #DBに挿入するデータリスト
    for account_id,account_name in zip(account_ids,account_names):

        account_url=base_url+"/"+account_name
        auto_twitter.access_url(account_url) #アカウントページにアクセス
        tweet_url=[]
        current_height=0
        scroll_num=0
        while len(tweet_url)<1 and scroll_num<3:
            result=auto_twitter.get_tweet(filters=[date_filter])
            if len(result)>0:
                tweet_url+=np.array(result)[:,0].tolist()
            current_height=auto_twitter.scroll_page(current_height,8)
            scroll_num+=1
        
        if len(tweet_url)>0:
            register_values+=[[idx+id_last,account_id,tweet_url.pop(0),now_datetime]]
            idx+=1
    print(register_values)
    #

    if len(register_values)==0: #新規tweetが無ければおしまい
        print("***No New Tweet...***")
        exit(1)
    

    #データベースに登録
    with conn:
        with conn.cursor() as cursor:
            query="""INSERT INTO tweet
                     (id,account_id ,url, get_time) VALUES(%s,%s,%s,%s);
                  """
            cursor.executemany(query,register_values)
        conn.commit()

if __name__=="__main__":
    main()

