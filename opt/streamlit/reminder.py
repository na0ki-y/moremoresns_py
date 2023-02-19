import json
import os
import schedule
from time import sleep
path_setting='./reminder_setting.json'
def make_setting_file():
    '''
    リマインダー設定ファイルのjsonがないときに作成
    '''
    afte_out_put={}
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

def task():
    print("タスク")

def setting(setting_json):
    '''
    スケジューラへ登録
    '''
    schedule.every(10).seconds.do(task)
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


if __name__=="__main__":
    main()