from openai import OpenAI
import streamlit as st
import time

assistant_id = st.secret["assistant_id"]
thread_id = st.secret["thread_id"]

with st.sidebar:
    st.link_button("더 좋은 컨텐츠를 만들어 갑니다. [br] 익명으로 후원하기", "https://toss.me/kimch8596")
    
    iframe_html = """쿠팡 파트너스 베너 링크"""
    st.markdown(iframe_html, unsafe_allow_html=True)
    st.info("이 포스팅은 어쩌고 저쩌고")
    st.caption('이 포스팅은 어쩌고 저쩌고.')

    openai_api_key = st.text_input("OpenAI API KEY", type="password")

    client = OpenAI(api_key=openai_api_key)

    thread_id = st.text_input("Thread ID", value=thread_id)

    thread_make_btn = st.button("Create a new thread")
    if thread_make_btn:
        thread = client.beta.threads.create()
        thread_id = thread.id
        st.subheader(f"{thread_id}", divider="rainbow")
        st.info("새로운 스레드가 생성되었습니다.")

st.title("My ChatBot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "저는 문화기획자 입니다. 무엇이든 물어보세요!?"}]

# print(f"st.session_state\n{st.session_state}")
# print()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input()
if prompt:
    # client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    response = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=prompt)

    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    # assistant_content = response.choices[0].message.content
    thread_messages = client.beta.threads.messages.list(thread_id)
    assistant_content = thread_messages.data[0].content[0].text.value

    st.session_state.messages.append({"role": "assistant", "content": assistant_content})
    st.chat_message("assistant").write(assistant_content)

    # print(st.session_state.messages)
