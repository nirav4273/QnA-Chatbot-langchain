
from main import llm
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from tool_funtion import add_number, divison, multiply_number, square, subsctract
import streamlit as st

agents = create_agent(
    tools=[add_number, multiply_number, square, subsctract, divison],
    model=llm,
    system_prompt="You are math teach and use tool for calculation"
)


st.title('QnA with Custom Agent tool')
st.markdown('AI QnA with custom tool execution which defined')


if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        st.chat_message('human').markdown(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message('ai').markdown(message.content)

st.chat_message("assistant").markdown('I am match teach to assist you.')
query = st.chat_input(placeholder="Ask your question")

if query:
    st.chat_message("human").markdown(query)

    st.session_state.messages.append(HumanMessage(content=query))

    response = agents.invoke({
        "messages": st.session_state.messages
    })

    messages = response["messages"]

    # Get the latest AI message
    ai_message = messages[-1]

    st.chat_message("ai").markdown(ai_message.content)
    st.session_state.messages.append(AIMessage(content=ai_message.content))
