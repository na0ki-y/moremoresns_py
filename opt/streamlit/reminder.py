import json
import os
import schedule
from time import sleep
import requests
from utils import load_data_url
path_setting='./reminder_setting.json'

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
    if not os.path.isfile(path_setting):
        make_setting_file()
    setting_json = json.load(open(path_setting, 'r'))
    return setting_json

def task(post_url):#スケジュールで登録された条件となったときににbrodcastへpost
    response = requests.post(post_url+"/broadcast")

def setting(post_url,setting_json):
    '''
    スケジューラへ登録
    '''
    if setting_json["10s"]:
        schedule.every(10).seconds.do(task,post_url=post_url)#10秒おき
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
    post_url=load_data_url()
    setting_json=load_setting()
    setting(post_url,setting_json)
    loop()


if __name__=="__main__":
    main()