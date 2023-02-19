import json
import os
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

def loop(setting_json):
    '''
    スケジューラの無限ループ
    '''
    pass
def main():
    setting_json=load_setting()
    loop(setting_json)

if __name__=="__main__":
    main()