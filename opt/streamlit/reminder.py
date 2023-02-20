import json
import os
import schedule
from time import sleep
import requests

path_setting='./reminder_setting.json'
URL_server="http://127.0.0.1:8000"#localのfastapiサーバ
def make_setting_file():
    '''
    リマインダー設定ファイルのjsonがないときに作成
    '''
    afte_out_put={"10s":True,"1h":False,"HH:MM":["08:00"]}
    with  open(path_setting, "w") as f:
            json.dump(afte_out_put, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
def load_setting():
    '''
    リマインダー設定ファイルのjsonを読み込む
    ignoreであるのでないときには、作成(make_setting_file())
    '''
    if not os.path.isfile('./reminder_setting.json'):
        make_setting_file()
    setting_json = json.load(open(path_setting, 'r'))
    return setting_json

def task():#スケジュールで登録された条件となったときににbrodcastへpost
    response = requests.post(URL_server+"/broadcast")

def setting(setting_json):
    '''
    スケジューラへ登録
    '''
    if setting_json["10s"]:
        schedule.every(10).seconds.do(task)#10秒おき
    if setting_json["1h"]:
        schedule.every(2).hours.do(task)#1時間おき
    for t in setting_json["HH:MM"]:
        schedule.every().day.at(t).do(task)#毎日XX:XX
def loop():
    '''
    スケジューラーの無限ループ
    '''
    while True:
        schedule.run_pending()
        sleep(1)
def main():
    setting_json=load_setting()
    setting(setting_json)
    loop()


if __name__=="__main__":
    main()