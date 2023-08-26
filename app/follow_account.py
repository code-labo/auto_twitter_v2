"""
アカウントをフォローする
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
from src.utils import add_single_quote


def main():
    print("Auto Follow")

    account_num_max=FOLLOW_ACCOUNT_CFG["ACCOUNT_NUM_MAX"]

    base_url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(base_url)


    ##フォロワーよりもフォロー中の数を増やしたくない
    ##ので、フォロワーの方が少なければ、フォローしない
    account_status=auto_twitter.get_status(base_url+f"/{ACCOUNT_NAME}")
    if account_status["num_follower"]-10<account_status["num_followed"]:
        print("*"*50)
        print(f"follower:{account_status['num_follower']}, followed:{account_status['num_followed']}")
        print("Auto Follow is canceled...")
        print("*"*50)
        exit(1)
    ##

    
    ##データベースへの接続
    conn=psycopg2.connect(
        host=HOST,user=USER,password=PASSWORD,database=DATABASE
    )

    #アカウント名を取得
    with conn:
        with conn.cursor() as cursor:
            except_account_query="("+",".join(map(add_single_quote,EXCEPT_ACCOUNT))+")"
            query=f"SELECT id,name FROM account WHERE roll='favoer' AND NOT name IN {except_account_query};"
            print(query)
            cursor.execute(query)
            accounts=np.array(cursor.fetchall())
        conn.commit()
    #

    if len(accounts)==0:
        print("***No account...***")
        exit(1)


    #フォローする
    choice_size=account_num_max if len(accounts)>account_num_max else len(accounts)
    idx_choiced=random.sample(
        np.arange(accounts.shape[0]).tolist(),choice_size
    )
    for _,account_name in accounts[np.array(idx_choiced)]:
        auto_twitter.follow(account_url=f"{base_url}/{account_name}")
    #

    #followしたアカウントのrollをfollowedに更新する
    with conn:
        with conn.cursor() as cursor:
            folloewd_ids=accounts[idx_choiced][:,0].reshape(-1,1).tolist() #favoしたツイートid
            query="UPDATE account SET roll='followed' WHERE id=%s;"
            cursor.executemany(query,folloewd_ids) #いいねしたやつを削除する
        conn.commit()
    #


if __name__=="__main__":
    main()