import streamlit as st

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