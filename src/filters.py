"""
投稿にフィルターをかけるメソッド
いいねしたくないときは,Trueを返す用にメソッドを作る
"""

import time
from datetime import datetime
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

from .envs import *


def hashtag_filter(article:WebElement)->bool:
    """
    ハッシュタグが多すぎるやついいねしちゃうと変だから,
    6個以上のやつはfilterにかける
    """
    
    pass


def date_filter(article:WebElement)->bool:
    """
    投稿が古すぎないかのフィルター

    1週間以上前の投稿はフィルターにかける
    """

    is_filter=False

    now=datetime.now() #今の時間

    element_time=article.find_element(by=By.TAG_NAME,value="time")
    dt=element_time.get_attribute("datetime")
    dt=re.sub("T(\d|\D)*","",dt)
    dt=datetime.strptime(dt,"%Y-%m-%d") #投稿された時間

    past_days=(now-dt).days #過ぎた日にち

    if past_days>7: #1週間以上経過していたらfilterにかける
        is_filter=True
    
    return is_filter


def bot_filter(article:WebElement)->bool:
    """
    記事がbotかどうか

    -return-
        is_bot:
            ボットならTrue
    """
    bot_words=["bot","Bot","BOT","ボット",ACCOUNT_NAME]+EXCEPT_ACCOUNT #これがアカウント名に入ってたらはじく(自分のも)

    is_bot=False

    elements_span=article.find_elements(by=By.TAG_NAME,value="span") #これのテキストにアカウント名と@名が入ってる
    #print(f"span num : {len(elements_span)}")
    for e in elements_span:

        try:
            ###テキストにbot_wordsがないか検索
            text=e.get_attribute("textContent")
            for b_word in bot_words:
                if b_word in text:
                    is_bot=True
                    break
            ###

            if is_bot==True:
                break
        except:
            continue

    #print(is_bot)

    return is_bot