"""
検索したツイートを取得
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import numpy as np
import pandas as pd

from src.auto_twitter import AutoTwitter
from src.filters import bot_filter


def main():
    url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(url=url)

    tweet_list=[]

    key_words=["#遊戯王"]
    tab_name="最新"
    for keyword in key_words:

        current_height=0

        auto_twitter.search_tweet(keyword="lang:ja "+keyword)
        auto_twitter.select_tab(tab_name=tab_name)

        for _ in range(3):
            tweet=auto_twitter.get_tweet(filters=[bot_filter])
            attrs=[[keyword,tab_name] for _ in range(len(tweet))]

            if len(tweet_list)==0:
                tweet_list=np.concatenate([
                    np.array(tweet),np.array(attrs)
                ],axis=1)
            else:
                tweet=np.concatenate([
                    np.array(tweet).reshape(-1,2),np.array(attrs)
                ],axis=1)
                tweet_list=np.concatenate([
                    tweet_list,tweet
                ],axis=0)
            current_height=auto_twitter.scroll_page(current_height=current_height)
            
    distinct_tweets=pd.DataFrame(
        np.unique(tweet_list,axis=0), #重複ツイートを削除
        columns=["url","account","keyword","tab_name"]
        )
    distinct_tweets.to_csv(f"{PARENT}/tweets.csv",index=False,encoding="utf-8_sig")

if __name__=="__main__":
    main()
