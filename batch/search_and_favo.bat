@echo off 

rem 再帰呼び出しで表示されなくする
@if not "%~0"=="%~dp0.\%~nx0" start /min cmd /c,"%~dp0.\%~nx0" %* & goto :eof

rem バッチファイルのあるディレクトリに移動
cd /d %~dp0

rem ひとつ上のディレクトリに移動
cd ../

rem anacondaをアクティブにする
call C:\Users\3meko\anaconda3\Scripts\activate.bat

rem 仮想環境をアクティブにする
call activate scraping_env 

python app/search_and_get_tweet.py
python app/favo_tweet.py --tweet_type searched

@REM pause