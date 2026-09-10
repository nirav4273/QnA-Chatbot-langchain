import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import SecretStr
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def upper(message: str):
    return message.upper()

def main() -> None:
    api_key = SecretStr(os.getenv("GROQ_API_KEY", ''))
    if not api_key:
        raise RuntimeError('Set GROQ_API_KEY first: $env:GROQ_API_KEY="your_api_key"')

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=api_key,
        temperature=1,
        max_tokens=8192,
        model_kwargs={"top_p": 0.95, "seed": 42},
    )
    parser = StrOutputParser() 
    prompt = ChatPromptTemplate.from_messages([
        {
            'role': 'system',
            'content': 'You are {lang} developer'
        },
        {
            'role': 'user',
            'content':  '{query}'
        }
    ])


    prompt_two = ChatPromptTemplate.from_messages([
        {
            'role': 'system',
            'content': 'Convert into short summary'
        },
        {
            'role': 'user',
            'content':  'Give short summary {query}'
        }
    ])

    """Way one to add this"""
    promptOne = prompt.invoke({'lang': 'JavaScript', 'query': 'Write basic LRU steps'})
    response = llm.invoke(promptOne)
   
    result = upper(parser.parse(str(response.content)))
    print(result)

    """
    Way via chaining
    """
    chain = prompt | llm | parser | upper 
    response = chain.invoke({'lang': 'JavaScript', 'query': 'Write basic LRU steps'})
    print(response)

if __name__ == "__main__":
    main()
