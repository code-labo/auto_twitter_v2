import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import numpy as np
import psycopg2
import argparse
import datetime
import random

from src.auto_twitter import AutoTwitter
from src.envs import *

def main():

    base_url="https://twitter.com"
    auto_twitter=AutoTwitter()
    auto_twitter.access_url(base_url)

    print(auto_twitter.get_status(base_url+f"/labo_code"))

if __name__=="__main__":
    main()