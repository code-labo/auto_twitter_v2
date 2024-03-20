"""
ツイートを検索し、DBにURLを保存する
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import numpy as np
from math import floor
from copy import deepcopy
import time
import pandas as pd

from src.auto_twitter import AutoTwitter
from src.filters import bot_filter
from src.envs import *
from src.utils import Color,print_view


def main():

    num_tweet_max=SEARCH_AND_GET_TWEET_CFG["NUM_TWEET_MAX"]
    key_words=SEARCH_AND_GET_TWEET_CFG["KEY_WORDS"]
    tab_names=SEARCH_AND_GET_TWEET_CFG["TAB_NAMES"]

    url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(url=url)

    saved_tweet_db=pd.read_csv(PARENT+"/database/tweets.csv",encoding="utf-8") #既に持ってるツイート

    #>> ツイートの検索 >>
    tweet_list=[]
    num_per_query=floor(num_tweet_max/len(key_words)/len(tab_names)) #1検索につき取るtweet数
    print("num_per_query",num_per_query)
    for tab_name in tab_names:
        for keyword in key_words:

            current_height=0

            auto_twitter.search_tweet(keyword="lang:ja "+keyword) #検索
            auto_twitter.select_tab(tab_name=tab_name) #タブ選択

            tweet_key_word=[]

            t=time.time()
            while len(tweet_key_word)<=num_per_query and (time.time()-t)<30: #30秒検索してたら次行く

                result=[]
                for tweet in auto_twitter.get_tweet(filters=[bot_filter]):
                    if not tweet[0] in saved_tweet_db["url"].values:
                        result+=[tweet]
                tweet_key_word+=result
                tweet_key_word=list(np.unique(tweet_key_word,axis=0)) #重複を削除

                current_height=auto_twitter.scroll_page(current_height=current_height)

            if len(tweet_key_word)>num_per_query:
                tweet_key_word=deepcopy(tweet_key_word[:num_per_query])
            tweet_list+=tweet_key_word
    #>> ツイートの検索 >>
    
    
    tweet_db=pd.DataFrame(tweet_list,columns=["url","account"])
    tweet_db["account"] = tweet_db["url"].str.extract(r'https://twitter.com/([^/]+)/status') #アカウント名を抽出

    priority=pd.Series(np.ones(shape=(tweet_db.shape[0])),name="priority")
    new_tweet_db = pd.concat([tweet_db, priority], axis=1)[["account","url","priority"]] #結合して列の順番を入れ替える

    print_view(
        "new_tweets",new_tweet_db,Color.CYAN
    )


    #>> 既に持っているtweetと結合し, 重複を消して保存 >>
    total_tweet_db=pd.concat([
        saved_tweet_db,new_tweet_db
    ])
    total_tweet_db.drop_duplicates(inplace=True)
    total_tweet_db.to_csv(f"{PARENT}/database/tweets.csv",encoding="utf-8",index=False)
    #>> 既に持っているtweetと結合し, 重複を消して保存 >>


if __name__=="__main__":
    main()

