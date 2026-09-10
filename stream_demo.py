from main import llm_stream
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate([
    {
        'role': 'system',
        'content': 'AI expert'
    },
    {
        'role': 'user',
        'content': '{query}'
    }
])

