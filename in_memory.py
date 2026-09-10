from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from langchain.agents import create_agent
from pydantic import SecretStr
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '')
if not TAVILY_API_KEY:
    raise RuntimeError('Set TAVILY_API_KEY first: $env:TAVILY_API_KEY="your_api_key"')

api_key = SecretStr(os.getenv("GROQ_API_KEY", ''))
if not api_key:
    raise RuntimeError('Set GROQ_API_KEY first: $env:GROQ_API_KEY="your_api_key"')

tavily_search_tool  = TavilySearch(
    max_results=5,
    # topic="general",
    # include_answer=False,
    include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    search_depth="basic",
    time_range="day",
    # include_domains=None,
    # exclude_domains=None
)

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key,
    temperature=1,
    max_tokens=8192,
    model_kwargs={"top_p": 0.95, "seed": 42},
    streaming=True
)

## Create memory
memory = MemorySaver()


# ## Need to create serper agent for google real search
agents = create_agent(
    system_prompt="You are assistant and give short ans",
    tools=[tavily_search_tool ],
    model=llm,
    checkpointer=memory ## Keep memory in story without managing self
)

while True:
    query = input()
    if query.lower() == 'exit':
        break

    response = agents.invoke({
        'messages': [
            {
                'role': 'user',
                'content': query
            }
        ]
    }, {
        'configurable': {
            'thread_id': '123'
        }
    })
    messages = response["messages"]

    print(messages[-1].content)

    