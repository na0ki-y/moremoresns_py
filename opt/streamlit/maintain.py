import streamlit as st
import requests


URL_server="https://7f8f-133-51-253-29.jp.ngrok.io"
URL_server="http://127.0.0.1:8000"
def main():
    if 'snstext' not in st.session_state: 
	    st.session_state.snstext = "None"
    st.title("MoreMoreSNS_maintain")
    if st.button("ブロードキャスト"):
        parm={"num":1}
        response = requests.post(URL_server+"/broadcast")
        print(response.status_code)    # HTTPのステータスコード取得
        print(response.text)    # レスポンスのHTMLを文字列で取得

if __name__=="__main__":
    main()