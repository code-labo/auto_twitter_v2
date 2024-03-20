"""
ツイートをいいねする
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import numpy as np
import random
import pandas as pd
from tqdm import tqdm

from src.auto_twitter import AutoTwitter
from src.envs import *
from src.utils import Color,print_view


def main():
    num_favo_max=FAVO_TWEET_CFG["NUM_FAVO_MAX"]

    tweet_db=pd.read_csv(f"{PARENT}/database/tweets.csv",encoding="utf-8")


    if tweet_db.shape[0]==0: #tweetが無ければ終わり
        print("***No tweet...***")
        exit(1)


    #>> favoするツイートを選ぶ >>
    choice_size=num_favo_max if tweet_db.shape[0]>num_favo_max else tweet_db.shape[0] #favoする数を決める

    target_tweets=tweet_db[tweet_db["priority"]>1.0] #まず優先度の高いツイートを取ってくる
    if target_tweets.shape[0]<choice_size: #優先度の高いツイートの数が少ないときは, 低い方からランダムに取ってくる
        low_priority_tweets=tweet_db[tweet_db["priority"]<=1.0] #優先度の低いツイートを取得
        idx_choiced=random.sample(
            np.arange(low_priority_tweets.shape[0]).tolist(),choice_size-target_tweets.shape[0] #ランダムサンプリング用のindexを準備
        )
        target_tweets=pd.concat(
            [target_tweets,low_priority_tweets.iloc[idx_choiced]] #サンプリングして結合
        )
    elif target_tweets.shape[0]>choice_size: #優先度の高いツイートが多い場合は切り捨てる
        target_tweets=target_tweets.iloc[:choice_size]

    print_view(
        "target_tweets",target_tweets,Color.CYAN
    )
    #>> favoするツイートを選ぶ >>


    #>> ツイートをfavo >>
    url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(url)

    with tqdm(total=target_tweets.shape[0]) as pbar:
        for _,tweet in target_tweets.iterrows():
            auto_twitter.favo(tweet["url"])
            pbar.update(1)
    #>> ツイートをfavo >>
        
    
    #>> fovoったツイートの削除 >>
    tweet_db.drop(target_tweets.index,inplace=True)
    tweet_db.reset_index(drop=True,inplace=True)
    tweet_db.to_csv(f"{PARENT}/database/tweets.csv",index=False,encoding="utf-8")
    #>> fovoったツイートの削除 >>


if __name__=="__main__":
    main()