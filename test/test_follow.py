"""
アカウントをフォローするテストコード
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import time
import numpy as np
import pandas as pd

from src.auto_twitter import AutoTwitter
from src.filters import bot_filter


def main():
    url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(url=url)


    #--ツイートを適当に検索
    tweet_list=[]
    key_words=["#b3d"]
    tab_name="話題"
    for keyword in key_words:

        current_height=0

        auto_twitter.search_tweet(keyword="lang:ja "+keyword)
        auto_twitter.select_tab(tab_name=tab_name)

        for _ in range(1):
            tweet_list+=auto_twitter.get_tweet(filters=[bot_filter])
            current_height=auto_twitter.scroll_page(current_height=current_height)

    tweet_db=pd.DataFrame(
        data=tweet_list,columns=["tweet_url","account_url"]
    )
    print(tweet_db)
    #--

    #--適当に1つ選んでフォロー
    account_url=np.random.choice(
        tweet_db["account_url"].values
    )
    auto_twitter.follow(account_url)
    time.sleep(5)
    #--
    
if __name__=="__main__":
    main()
