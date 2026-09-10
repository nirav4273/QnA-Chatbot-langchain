from main import llm
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


@tool
def add_number(a:int, b: int):
    """
    It will return sum of two numbers.
    Args:
        a: Number one
        b: Number two
    """
    return a + b


@tool
def multiply_number(a:int, b: int):
    """
    It will return multiplication of two numbers.
    Args:
        a: Number one
        b: Number two
    """
    return a * b

@tool
def square(a:int):
    """
    It will return square of given number.
    Args:
        a: Number one
    """
    return a ** a


agents = create_agent(
    tools=[add_number, multiply_number, square],
    model=llm,
    system_prompt="You are math teach and use tool for calculation"
)


messages = []

while True:
    query = input('Ask:  ')
    if query.lower() == 'break':
        break;
    messages.append(HumanMessage(query))
    response = agents.invoke({
        "messages": messages
    })

    # # Update history with agent-generated messages
    messages = response["messages"]

    for result in response['messages']:
        print(result.content)
        print("\n")
    
