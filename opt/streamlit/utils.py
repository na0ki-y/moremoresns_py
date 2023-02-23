import json 
import os
path_url='./global_url.json'
def make_url_file():
    '''
    グローバルURL設定ファイルのjsonがないときに作成
    '''
    afte_out_put={"url_global":"None","url_local":"http://127.0.0.1:8000"}
    with  open(path_url, "w") as f:
            json.dump(afte_out_put, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
def load_url():
    '''
    グローバルURLファイルのjsonを読み込む
    ignoreであるのでないときには、作成(make_url_file())
    '''
    if not os.path.isfile(path_url):
        make_url_file()
    url_json = json.load(open(path_url, 'r'))
    return url_json
def load_data_url():
    '''
    jsonにglobalが書いてあればglobal
    なければlocalを返す
    '''
    url_json=load_url()
    if url_json["url_global"]=="None":
        print("local")
        return url_json["url_local"]
    else:
        print("global")
        return url_json["url_global"]
if __name__=="__main__":
    load_url()
    print("utils")