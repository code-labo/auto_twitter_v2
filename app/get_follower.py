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
import pandas as pd

from src.auto_twitter import AutoTwitter
from src.envs import *

def main():

    max_minutes=GET_FOLLOWER_CFG["max_minutes"]


    account_db=pd.read_csv(f"{PARENT}/database/accounts.csv") #既に登録したアカウントを読み込み


    #>> フォロワーの取得 >>
    url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(url)
    
    follower_link_list=auto_twitter.get_follower_links(
        account_url=f"{url}/{ACCOUNT_NAME}",max_minutes=max_minutes
    )

    new_follower=[]
    for link in follower_link_list:

        name=link.replace("https://twitter.com/","")
        if len(account_db[account_db["name"]==name])==0: #まだ登録されていないとき
            access_at=datetime.datetime.now()-datetime.timedelta(days=365*10) #まだアクセスしてないので, すごく昔の時間を登録しとく
            is_followed=True
            is_following=False
            is_favo=False
            new_follower+=[[
                name,is_following,is_followed,
                is_favo,access_at
            ]]
        elif len(account_db[account_db["name"]==name])>0: #登録済みのとき
            pass
    #>> フォロワーの取得 >>
    

    #>> 登録 >>
    new_follower_db=pd.DataFrame(
        new_follower,columns=["name","is_following","is_followed","is_favo","access_at"]
    )
    print("new followers"+"-"*50)
    print(new_follower_db)
    account_db=pd.concat(
        [account_db,new_follower_db]
    )
    account_db.to_csv(f"{PARENT}/database/accounts.csv",index=False,encoding="utf-8")
    #>> 登録 >>


if __name__=="__main__":
    
    main()