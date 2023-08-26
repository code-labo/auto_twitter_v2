"""
あるアカウントのフォロワーを取得
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

from src.auto_twitter import AutoTwitter


def main():
    url="https://twitter.com"
    url="https://twitter.com/3meko1"
    auto_twitter=AutoTwitter()
    
    follower_list=auto_twitter.get_follower_links(
        account_url=url
    )
    print(follower_list)
    print(len(follower_list))
    

if __name__=="__main__":
    
    main()