"""
自分のアカウントのフォロワーを取得
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import datetime
import pandas as pd

from src.auto_twitter import AutoTwitter
from src.envs import *
from src.utils import Color

def main():

    max_minutes=GET_FOLLOWER_CFG["max_minutes"]


    url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(url)
    

    #>> フォロワー名の取得 >>
    obtained_accounts=[
        link.replace("https://twitter.com/","") for link
        in auto_twitter.get_follower_links(
                account_url=f"{url}/{ACCOUNT_NAME}",max_minutes=max_minutes
            )
    ]
    #>> フォロワー名の取得 >>


    accounts=pd.read_csv(f"{PARENT}/database/accounts.csv",encoding="utf-8") #既に登録されたアカウントを読み出し
    

    #>> 既に持ってるアカウントのis_follwedをTrueに >>
    owned_accounts=accounts[
        (accounts["name"].isin(obtained_accounts))
    ]
    for record_idx,record in owned_accounts.iterrows():
        accounts.at[record_idx,"is_followed"]=True
    msg="-"*40+f"{Color.CYAN}update accounts{Color.RESET}"+"-"*40
    print(f"{msg}\n{owned_accounts}\n{'-'*(len(msg)-len(f'{Color.CYAN}{Color.RESET}'))}")
    #>> 既に持ってるアカウントのis_followedをTrueに >>


    #>> 新しいアカウントを追加 >>
    new_accounts=[]
    for account in obtained_accounts:
        if owned_accounts.shape[0]>0:
            if not account in owned_accounts["name"].values:
                access_at=datetime.datetime.now()-datetime.timedelta(days=365*10) #まだアクセスしてないので, すごく昔の時間を登録しとく
                new_accounts+=[
                    [account,False,True,False,access_at]
                ]
        else:
            access_at=datetime.datetime.now()-datetime.timedelta(days=365*10) #まだアクセスしてないので, すごく昔の時間を登録しとく
            new_accounts+=[
                [account,False,True,False,access_at]
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