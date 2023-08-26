import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time


def init_driver(driver_dir,profile_path,profile_name):

    ##バックグラウンドで実行する際のオプション
    ##コメント外すとバックグラウンドで実行される
    options=Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument(f"--profile-directory={profile_name}")
    ##
    driver=webdriver.Edge(executable_path=driver_dir,options=options) #driverをセット
    driver.set_window_size(1280,720)
    driver.implicitly_wait(5)
    time.sleep(3)
    return driver
