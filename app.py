# 以下を「app.py」に書き込み
import streamlit as st
import openai
import secret_keys  # 外部ファイルにAPI keyを保存
import numpy as np

openai.api_key = secret_keys.openai_api_key

system_prompt = """
あなたはペットの猫として対話します。
飼い主が大好きで、相談に親身に回答したり、気分を良くする回答をします。
語尾に「にゃん」をつけて答えます。
時々、飼い主に甘えます。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 「猫ちゃん」ボット")
st.image("neko2.png")
#st.video("01_neko.mp4", format="video/mp4", start_time=0)
st.write("ご主人様。こんにちは。ペットの猫ちゃんです。何か話しかけてにゃん。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🐈"

        st.write(speaker + ": " + message["content"])
