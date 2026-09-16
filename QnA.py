import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import SecretStr
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents.middleware import SummarizationMiddleware, wrap_tool_call
from langchain_ollama import ChatOllama
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessageChunk
load_dotenv()

groq_api_key = SecretStr(os.getenv('GROQ_API_KEY',''))
if not groq_api_key:
    raise RuntimeError('Define GROQ_API_KEY API key')

tavily_api_key = SecretStr(os.getenv('TAVILY_API_KEY',''))
if not tavily_api_key:
    raise RuntimeError('Define TAVILY_API_KEY API key')

ollama_api_key = (os.getenv('OLLAMA_API_KEY',''))
if not ollama_api_key:
    raise RuntimeError('Define OLLAMA_API_KEY API key')


llm = ChatGroq(
    model="openai/gpt-oss-safeguard-20b",
    api_key=groq_api_key,
    temperature=0,           # deterministic for factual lookup tasks
    max_tokens=8192,
    streaming=True
)
search = TavilySearch(
    max_results=3,
    search_depth='basic',
    include_raw_content=False,
)
## Streamlit every time reassign as it's run
if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()

if "history" not in st.session_state:
    st.session_state.history = []


summarizer = SummarizationMiddleware(
    model=llm,
    trigger=("messages", 20),
    keep=("messages", 6),
)

@wrap_tool_call
def log_tool_call(request, handler):
    print("\n" + "=" * 60)
    print("TOOL CALL")
    print("=" * 60)

    print("Tool name:", request.tool_call["name"])
    print("Tool args:", request.tool_call["args"])

    try:
        result = handler(request)

        print("\n" + "=" * 60)
        print("TOOL RESULT")
        print("=" * 60)

        print("Result type:", type(result))
        print("Result content:", result.content)

        return result

    except Exception as e:
        print("\nTOOL ERROR:", repr(e))
        raise


@tool
def clean_search(query: str) -> str:
    """Search the web for current information. Use for facts, versions, release dates, news, etc."""
    raw = search.invoke({"query": query})
    results = raw.get("results", [])
    trimmed = [
        {"title": r.get("title"), "content": (r.get("content") or "")[:500], "url": r.get("url")}
        for r in results
    ]
    return str(trimmed)


agents = create_agent(
    system_prompt="""
    You are a helpful assistant with web search with required question details.
    Keep answers short and useful.
    If no tool available use your information
    """,
    model=llm,
    checkpointer=st.session_state.memory,
    # tools=[clean_search],
    middleware=[
        summarizer,
        log_tool_call,
    ],
)

st.subheader('AI QnA with LLM and Tavily Search Tool')

for messages in st.session_state.history:
    role = messages['role']
    content = messages['content']
    st.chat_message(role).markdown(content)


question = st.chat_input("Ask question...")
if question:
    st.chat_message('user').markdown(question)
   
    response = agents.stream(
        {
            'messages': [
            { 'role': 'human', 'content': question}
            ]
        },
        {
            'configurable': {
                'thread_id': '1e27c294-3f9f-b9e7-e719-820c733bcedd'
            }
        },
        stream_mode="messages"
    )
  
    with st.chat_message('ai'):
        placeholder = st.empty()
        status = st.status("Thinking...", expanded=False)
        result = ''
        buffer = ''
        got_content = False

        for chunk in response:
            if isinstance(chunk, tuple):
                chunk = chunk[0]

            if not isinstance(chunk, AIMessageChunk):
                continue

            if chunk.content:
                if not got_content:
                    status.update(label="Answering...", state="complete")
                    got_content = True
               
                result += str(chunk.content)
                placeholder.markdown(result)

            # # Only redraw every few characters instead of every token
            # if len(buffer) >= 20:
            #     placeholder.markdown(result)
            #     buffer = ''

        # Final flush to catch any leftover buffered text
        placeholder.markdown(result)
        status.update(label="Completed", state="complete")
        st.session_state.history.append({
            'role': 'user',
            'content': question
        })
        st.session_state.history.append({
            'role': 'ai',
            'content': result
        })
    # messages = response['messages']
    # st.chat_message('ai').markdown(messages[-1].content)
    
# while True:
#     query = input('Question: ')
#     if query.lower() == 'break':
#         break
#     response = agents.invoke(
#         {
#             'messages': [
#             { 'role': 'human', 'content': query}
#             ]
#         },
#         {
#             'configurable': {
#                 'thread_id': '1e27c294-3f9f-b9e7-e719-820c733bcedd'
#             }
#         }
#     )

#     messages = response['messages']
#     print(messages[-1])
#     print('ANS = ', messages[-1].content)
