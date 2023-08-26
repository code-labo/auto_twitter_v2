"""
自分のアカウントのフォロワーを取得
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import psycopg2
import numpy as np
import datetime

from src.auto_twitter import AutoTwitter
from src.envs import *

def main():

    max_minutes=GET_FOLLOWER_CFG["max_minutes"]

    ##既に登録済みのメンバー(follower)を取得
    conn=psycopg2.connect(
        host=HOST,user=USER,password=PASSWORD,database=DATABASE
    )
    with conn:
        with conn.cursor() as cursor:

            #既に登録済みのフォロワー
            query=f"""SELECT name FROM account 
                     WHERE roll='follower';"""
            cursor.execute(query)
            result=np.array(cursor.fetchall())
            member_name_db=[name.replace(" ","") for name in result.flatten()]
            #

            #最大idの取得.自動で振り分けされない.なんでや
            query="SELECT MAX(id) FROM account;"
            cursor.execute(query)
            result=cursor.fetchone()
            id_last=int(result[0]) if not result[0] is None else 0
            #
            
        conn.commit()
    ##

    url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(url)
    
    follower_link_list=auto_twitter.get_follower_links(
        account_url=f"{url}/{ACCOUNT_NAME}",max_minutes=max_minutes
    )
    all_follower_names=[link.replace("https://twitter.com/","") for link in follower_link_list]
    new_followers=[]
    idx=1
    for follower_name in all_follower_names:
        if not follower_name in member_name_db:
            new_followers+=[[id_last+idx,follower_name,datetime.datetime.now()-datetime.timedelta(days=365*10)]]
            idx+=1
    # print(all_follower_names)
    # print(new_followers)

    #登録
    with conn:
        with conn.cursor() as cursor:
            query="""INSERT INTO account 
                     (id,name,roll,favo_at)
                     VALUES(%s,%s,'follower',%s);"""
            cursor.executemany(query,new_followers)
        conn.commit() 

if __name__=="__main__":
    
    main()