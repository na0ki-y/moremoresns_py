import streamlit as st
import requests
from utils import load_data_url
URL_server_local="http://127.0.0.1:8000"#localのfastapiサーバ
@st.cache_data  # 👈 Add the caching decorator
def load_data_cache_url():
    return load_data_url()
def main():
    if 'snstext' not in st.session_state: 
	    st.session_state.snstext = "None"
    post_url=load_data_cache_url()
    st.title("MoreMoreSNS_maintain")
    if st.button("ブロードキャスト"):#ボタンが押されたときにbrodcastへpost
        parm={"num":1}
        response = requests.post(post_url+"/broadcast")
        print(response.status_code)    # HTTPのステータスコード取得
        print(response.text)    # レスポンスのHTMLを文字列で取得

if __name__=="__main__":
    main()