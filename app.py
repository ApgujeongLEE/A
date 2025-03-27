try:
    import streamlit as st
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'streamlit' package is not installed. Please install it using 'pip install streamlit' and try again.")

from chatbot import get_apartment_info
from datetime import datetime

st.set_page_config(page_title="서울 부동산 챗봇", page_icon="\U0001F3E0", layout="centered")
st.markdown("""
    <style>
        .chat-container {
            background-color: #f9f9f9;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            min-height: 500px;
        }
        .chat-bubble-user {
            background-color: #e0f7fa;
            padding: 10px 15px;
            border-radius: 15px;
            margin-bottom: 8px;
            display: inline-block;
            max-width: 80%;
        }
        .chat-bubble-bot {
            background-color: #fff3e0;
            padding: 10px 15px;
            border-radius: 15px;
            margin-bottom: 20px;
            display: inline-block;
            max-width: 80%;
        }
    </style>
""", unsafe_allow_html=True)

st.title("\U0001F3E0 서울 아파트 시세 챗봇")
st.caption("실거래가 기반 서울 아파트 시세를 알려드립니다.")

with st.form(key="chat_form"):
    user_input = st.text_input(
        "\U0001F4AC 질문을 입력하세요",
        "",
        placeholder="예: 래미안장위퍼스트하이 84평 매매가",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("질문하기")

if submitted and user_input:
    response = get_apartment_info(user_input)
    st.session_state.chat_history.append((user_input, response))

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for q, r in st.session_state.chat_history[::-1]:
    st.markdown(f"<div class='chat-bubble-user'>🙋‍♂️ 사용자: {q}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble-bot'>🤖 챗봇: {r}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""---\n<small>업데이트 시각: {}</small>""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
