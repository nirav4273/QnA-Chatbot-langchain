import streamlit as st
from main import llm

st.title('AI QnA bot')
st.markdown('AI QnA with keep memory of last questions.')

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
    response = llm.invoke(st.session_state.messages)
    st.session_state.messages.append({'role': 'ai', 'content': response.content})
    st.chat_message('ai').markdown(response.content)
