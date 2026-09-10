from langchain_core.tools import tool


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

@tool
def subsctract(a:int, b: int):
    """
    Subtract b from a.
    Args:
        a: First number.
        b: Number to subtract from a.
    """
    return a - b

@tool
def divison(a:int, b: int):
    """
    It will return divison of given number.
    Args:
        a: Number one
        b: Number two
    """
    return a / b