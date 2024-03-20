"""
自分のツイートにいいねした人をfavoerとしてDBにpush
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import numpy as np
import pandas as pd
import datetime

from src.auto_twitter import AutoTwitter
from src.envs import *
from src.filters import date_filter
from src.utils import Color

def main():
    tweet_num=GET_FAVOER_CFG["TWEET_NUM"] #取得するツイートの数
    max_account_num=GET_FAVOER_CFG["ACCOUNT_NUM_MAX"]


    base_url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(f"{base_url}/{ACCOUNT_NAME}")

    ##>> 今の画面のツイートをtweet_num件取得 >>
    tweets=[]
    current_height=0
    is_update=True
    while len(tweets)<tweet_num and is_update:

        prev_tweet_num=len(tweets)

        tweets+=auto_twitter.get_tweet(
            filters=[date_filter]
        ) #ツイートの取得
        tweets=list(np.unique(tweets,axis=0)) #重複を削除

        current_height+=auto_twitter.scroll_page(current_height) #ページをスクロール

        now_tweet_num=len(tweets) 
        if prev_tweet_num==now_tweet_num: #更新がなければおしまい
            is_update=False

    tweets=np.array(tweets)
    ##>> 今の画面のツイートをtweet_num件取得 >>


    ##>> 取得したツイートにいいねした人を取得 >>
    obtained_accounts=[]
    for tweet_url,_ in tweets:
        names_on_tweet=[
            link.replace(r"https://twitter.com/","") for link 
            in auto_twitter.get_favoers(tweet_url=tweet_url,max_account_num=max_account_num)
            ]
        obtained_accounts+=names_on_tweet
    ##>> 取得したツイートにいいねした人を取得 >>


    accounts=pd.read_csv(f"{PARENT}/database/accounts.csv",encoding="utf-8") #既に登録されたアカウントを読み出し
    

    #>> 既に持ってるアカウントのis_favoをTrueに >>
    owned_accounts=accounts[
        accounts["name"].isin(obtained_accounts) #既に持ってるかつ、取得したアカウントを取得
    ] 
    for record_idx,record in owned_accounts.iterrows():
        accounts.at[record_idx,"is_favo"]=True
    msg="-"*40+f"{Color.CYAN}update accounts{Color.RESET}"+"-"*40
    print(f"{msg}\n{owned_accounts}\n{'-'*(len(msg)-len(f'{Color.CYAN}{Color.RESET}'))}")
    #>> 既に持ってるアカウントのis_favoをTrueに >>
        

    #>> 新しいアカウントを追加 >>
    new_accounts=[]
    for account in obtained_accounts:
        if not account in owned_accounts["name"].values:
            access_at=datetime.datetime.now()-datetime.timedelta(days=365*10) #まだアクセスしてないので, すごく昔の時間を登録しとく
            new_accounts+=[
                [account,False,False,True,access_at]
            ]
    new_accounts=pd.DataFrame(
        new_accounts,
        columns=["name","is_following","is_followed","is_favo","access_at"]
    )
    msg="-"*40+f"{Color.MAGENTA}new accounts{Color.RESET}"+"-"*40
    print(f"{msg}\n{new_accounts}\n{'-'*(len(msg)-len(f'{Color.CYAN}{Color.RESET}'))}")
    #>> 新しいアカウントを追加 >>


    #>> テーブルにnew_accountを追加して保存 >>
    accounts=pd.concat(
        [accounts,new_accounts]
    )
    accounts.to_csv(f"{PARENT}/database/accounts.csv",index=False,encoding="utf-8")
    #>> テーブルにnew_accountを追加して保存 >>


if __name__=="__main__":
    main()