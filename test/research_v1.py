"""
画面のHTMLを保存するコード
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

import re
import json

from src.auto_twitter import AutoTwitter

def main():

    # https://twitter.com/TAKOYAKIUMEEee/status/1662440397338214402

    url="https://twitter.com/ovoshokora"

    auto_twitter=AutoTwitter()
    auto_twitter.access_url(url)

    html=auto_twitter.driver.page_source
    with open(f"{PARENT}/research.html","w",encoding="utf-8") as f:
        soup=BeautifulSoup(html,"html.parser")
        f.write(soup.prettify())
        print("save done")

    # articles=driver.find_elements(by=By.TAG_NAME,value="article")
    # for i,article in enumerate(articles):
    #     print(f"article{i+1}")
    #     anchers=article.find_elements(by=By.TAG_NAME,value="a")
    #     for a in anchers:
    #         href=a.get_attribute("href")
    #         if a.get_attribute("dir") and ("status" in href):
    #             account=re.sub("status.*","",href) #ツイート持ち主のアカウント
    #             print(href) #←ツイートのurl
    #             print(account)

    #     #--これでいいねボタンをチェックできる
    #     buttons=article.find_elements(
    #         By.CLASS_NAME,
    #         value="css-18t94o4.css-1dbjc4n.r-1777fci.r-bt1l66.r-1ny4l3l.r-bztko3.r-lrvibr"
    #         )
    #     # print(buttons)
    #     for button in buttons:
    #         if "いいね" in button.get_attribute("aria-label"):
    #             print(button) #<-いいねボタン
    #             # button.click() #<-これでクリックできる
    #     #--



if __name__=="__main__":
    main()
    