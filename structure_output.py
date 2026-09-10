from typing import Literal, cast

from main import llm
from pydantic import Field,BaseModel

class User(BaseModel):
    name: str = Field(description="Full name of user")
    age: int = Field(description="Age of the user")
    email: str = Field(description="Email id of the user")

class ResponseStructure(BaseModel):
    type: Literal["single", "array"]#
    data: User | list[User]

query = """My name is Rahul Sharma and I am 28 years old. You can reach me at rahul.sharma@gmail.com.

Priya Patel is 32 years old. Her email address is priya.patel@yahoo.com.

John Smith, age 41, uses john.smith@outlook.com for communication.

Neha is 25 and her email is neha123@gmail.com.

Amit Kumar is 35 years old and can be contacted at amit.kumar@company.com."""


def execute() -> None:
    model = llm.with_structured_output(ResponseStructure)
    respose = model.invoke(query + ' Extract data in correct format and 1 user return only')
    result = cast(ResponseStructure, respose);
    print(result.model_dump())

execute()