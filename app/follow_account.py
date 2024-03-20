"""
favoってくれた人 or followしてくれた人をフォローする
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import pandas as pd

from src.auto_twitter import AutoTwitter
from src.envs import *
from src.utils import Color, print_view


def main():
    print("Auto Follow")

    account_num_max=FOLLOW_ACCOUNT_CFG["ACCOUNT_NUM_MAX"]


    accounts=pd.read_csv(f"{PARENT}/database/accounts.csv")
    target_accounts=accounts[
        ((accounts["is_favo"]==True) & (accounts["is_following"]==False))
        | ((accounts["is_followed"]==True) & (accounts["is_following"]==False))
    ].iloc[:account_num_max]
    print_view(
        table_name="target_account",table=target_accounts,color=Color.MAGENTA
    )


    base_url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(base_url)


    #フォロワーよりもフォロー中の数を増やしたくない
    #ので、フォロワーの方が少なければ、フォローしない
    account_status=auto_twitter.get_status(base_url+f"/{ACCOUNT_NAME}")
    if account_status["num_follower"]-10<account_status["num_followed"]:
        print("*"*50)
        print(f"follower:{account_status['num_follower']}, followed:{account_status['num_followed']}")
        print("Auto Follow is canceled...")
        print("*"*50)
        exit(1)
    #

    if target_accounts.shape[0]==0:
        print("***No account...***")
        exit(1)


    #>> フォローする >>
    for record_idx,record in target_accounts.iterrows():
        auto_twitter.follow(
            account_url=f"{base_url}/{record['name']}"
        )
        accounts.at[record_idx,"is_following"]=True
    #>> フォローする >>
        

    #>> accountテーブルの更新 >>
    accounts.to_csv(f"{PARENT}/database/accounts.csv",index=False,encoding="utf-8")
    #>> accountテーブルの更新 >>


if __name__=="__main__":
    main()