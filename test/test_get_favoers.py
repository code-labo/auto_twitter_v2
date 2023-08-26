"""
あるツイートにいいねした人を取得
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

from bs4 import BeautifulSoup

from src.auto_twitter import AutoTwitter
from src.filters import bot_filter


def main():
    url="https://twitter.com"
    auto_twitter=AutoTwitter()
    
    favoer_list=auto_twitter.get_favoers(
        tweet_url="https://twitter.com/3meko1/status/1558442352657977346/"
    )

    print(favoer_list)
    print(len(favoer_list))

    html=auto_twitter.driver.page_source
    with open("research.html","w",encoding="utf-8") as f:
        soup=BeautifulSoup(html,"html.parser")
        f.write(soup.prettify())
        print("save done")

if __name__=="__main__":
    main()