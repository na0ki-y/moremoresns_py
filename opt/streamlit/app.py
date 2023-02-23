import streamlit as st


path_global='./reminder_setting.json'
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
def main():
    if 'snstext' not in st.session_state: 
	    st.session_state.snstext = "None"
    st.title("moremoresns")
    st.markdown("# Step1: 質問にこたえよう ")
    
    st.session_state.snstext = st.selectbox(
    '今日食べたものは？',
    ('パン', 'ご飯', 'パスタ'))
    st.markdown("# Step2: SNSへとぶ ")
    st.write("{}".format(st.session_state.snstext))
    st.write("[Tweet](https://twitter.com/intent/tweet?text={}をたべたよ)".format(st.session_state.snstext))

if __name__=="__main__":
    main()