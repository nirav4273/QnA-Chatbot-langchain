import streamlit as st
from main import llm_stream

st.title('AI QnA bot')

query = st.chat_input()
if 'messages' not in st.session_state:
    st.session_state.messages = []

for messages in st.session_state.messages:
    role = messages['role']
    content = messages['content']
    st.chat_message(role).markdown(content)

if query:
    st.session_state.messages.append({'role': 'user', 'content': query})
    st.chat_message('user').markdown(query)
    response = llm_stream.stream(st.session_state.messages)
    result = ''
    with st.chat_message("ai"):
        placeholder = st.empty()

        for chunk in response:
            content = chunk.content

            if isinstance(content, str):
                result += content

            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, str):
                        result += item
                    elif isinstance(item, dict) and item.get("type") == "text":
                        result += item.get("text", "")

            placeholder.markdown(result)

    st.session_state.messages.append({'role': 'ai', 'content': result})
    # result = ''
    # for chunk in response:
    #     # st.session_state.messages.append({'role': 'ai', 'content': chunk.content})
    #     # result += chunk.content
    #     st.chat_message('ai').markdown(chunk.content)
