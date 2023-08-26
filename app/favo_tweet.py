"""
ツイートをいいねする
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import numpy as np
import psycopg2
import argparse
import datetime
import random

from src.auto_twitter import AutoTwitter
from src.envs import *


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--tweet_type",default="searched")
    args=parser.parse_args()

    num_favo_max=FAVO_TWEET_CFG["NUM_FAVO_MAX"]

    now=datetime.datetime.now()

    ##データベースへの接続
    conn=psycopg2.connect(
        host=HOST,user=USER,password=PASSWORD,database=DATABASE
    )

    #ツイートを取得
    with conn:
        with conn.cursor() as cursor:

            if args.tweet_type=="searched": #検索したツイート
                query="SELECT id,url FROM tweet WHERE account_id IS NULL;"
                cursor.execute(query)
                tweets=np.array(cursor.fetchall())

            elif args.tweet_type=="follower": #フォロワーのツイート
                query="""SELECT id,account_id,url FROM tweet
                         WHERE NOT account_id IS NULL;
                      """
                cursor.execute(query)
                result=np.array(cursor.fetchall())
                if len(result)>0:
                    tweets=np.concatenate(
                        [result[:,0].reshape(-1,1),result[:,2].reshape(-1,1)],
                        axis=1
                    )
                    account_ids=result[:,1]
                else:
                    tweets=result
        conn.commit()
    #

    if len(tweets)==0: #tweetが無ければ終わり
        print("***No tweet...***")
        exit(1)

    url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(url)

    #いいねする
    choice_size=num_favo_max if len(tweets)>num_favo_max else len(tweets)
    idx_choiced=random.sample(
        np.arange(tweets.shape[0]).tolist(),choice_size
    )
    for _,tweet_url in tweets[np.array(idx_choiced)]:
        auto_twitter.favo(tweet_url)
    print("---")
    print("Favo following tweets")
    print(tweets[idx_choiced])

    #

    #favoったツイートを削除する
    with conn:
        with conn.cursor() as cursor:
            deleted_ids=tweets[idx_choiced][:,0].reshape(-1,1).tolist() #favoしたツイートid
            query="DELETE FROM tweet WHERE id=%s;"
            cursor.executemany(query,deleted_ids) #いいねしたやつを削除する
        
            if args.tweet_type=="follower": #followerツイートの場合は,favo時間を登録する
                query="""UPDATE account
                         SET favo_at=%s
                         WHERE id=%s;
                      """
                values=[[now,account_id] for account_id in account_ids]
                cursor.executemany(query,values)
        
        conn.commit()
    #


if __name__=="__main__":
    main()