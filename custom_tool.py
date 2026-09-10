from main import llm
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from tool_funtion import add_number,  multiply_number, square

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
    
