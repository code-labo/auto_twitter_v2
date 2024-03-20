"""
ツイートを検索し、DBにURLを保存する
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import numpy as np
from datetime import datetime
import pandas as pd

from src.auto_twitter import AutoTwitter
from src.filters import date_filter
from src.envs import *
from src.utils import Color,print_view


def main():

    num_account=GET_FOLLOWERS_TWEET_CFG["NUM_ACCOUNT"]
    now=datetime.now()

    accounts=pd.read_csv(f"{PARENT}/database/accounts.csv")
    followers=accounts[accounts["is_followed"]==True]
    target_followers=followers.sort_values(by="access_at",ascending=True).iloc[:num_account] #昇順に並び替え

    print_view(
        "target followers",target_followers,Color.MAGENTA
    )

    base_url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(url=base_url)


    #>> 1つのアカウントにつき最新のツイートを1つ取ってくる (あれば) >>
    register_values=[] #DBに挿入するデータリスト
    for account_id,account_record in target_followers.iterrows():

        account_url=base_url+"/"+account_record["name"]
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
            register_values+=[[account_record["name"],tweet_url.pop(0),3.0]]
    print(register_values)
    #>> 1つのアカウントにつき最新のツイートを1つ取ってくる (あれば) >>

    if len(register_values)==0: #新規tweetが無ければおしまい
        print("***No New Tweet...***")
        exit(1)

    #>> accountテーブルのアクセス時間の更新 >>
    for record_idx, record in target_followers.iterrows():
        accounts.at[record_idx,"access_at"]=now
    accounts.to_csv(f"{PARENT}/database/accounts.csv",index=False,encoding="utf-8")
    #>> accountテーブルのアクセス時間の更新 >>
    
    #>> tweetテーブルに新規追加 >>
    new_tweets=pd.DataFrame(
        register_values,columns=["account","url","priority"]
    )
    tweets=pd.read_csv(f"{PARENT}/database/tweets.csv",encoding="utf-8")
    tweets=pd.concat(
        [tweets,new_tweets]
    )
    tweets.drop_duplicates(inplace=True) #一応重複を消す
    tweets.to_csv(f"{PARENT}/database/tweets.csv",index=False,encoding="utf-8")

    print_view(
        "new_tweets",new_tweets,Color.CYAN
    )
    #>> tweetテーブルに新規追加 >>

if __name__=="__main__":
    main()

