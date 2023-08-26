"""
自分のアカウントを挿入
"""

import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import psycopg2
from src.envs import *

OWNER_QUERY="""INSERT INTO account 
                (id ,name ,url,roll) 
                VALUES (1,'labo_code','https://twitter.com/labo_code', 'owner');"""

TEST_QUERY="""INSERT INTO account 
              (id ,name ,url,roll)
              VALUES (2,'MSTER_BA','https://twitter.com/MSTER_BA', 'favoer');"""

def main():

    ##データベースへの接続
    conn=psycopg2.connect(
        host=HOST,user=USER,password=PASSWORD,database=DATABASE
    )

    with conn:
        with conn.cursor() as cursor:

            query=TEST_QUERY
            cursor.execute(query)
            #

        conn.commit()


if __name__=="__main__":
    main()

