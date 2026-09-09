import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import SecretStr

load_dotenv()

def main() -> None:
    api_key = SecretStr(os.getenv("GROQ_API_KEY", ''))
    if not api_key:
        raise RuntimeError('Set GROQ_API_KEY first: $env:GROQ_API_KEY="your_api_key"')

    client = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=api_key,
        temperature=1,
        max_tokens=8192,
        model_kwargs={"top_p": 0.95, "seed": 42},
    )

    promps = [
        ('system', 'You are GoLang developer'),
        ('user', 'Need to generate LRU basic flow')
    ]

    response = client.invoke(promps)
    print(response.content)


if __name__ == "__main__":
    main()
