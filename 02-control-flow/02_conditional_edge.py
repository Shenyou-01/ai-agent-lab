from typing import TypedDict
from langgraph.graph import StateGraph , START , END

class State(TypedDict):
    message: str
    route: str

def hello(state: State):
    return {
        "message": state["message"] + " Hello"
    }


def world(state: State):
    return {
        "message": state["message"] + " World"
    }

def router(state:State):
    if "hello" in state["route"]:
        return "hello"
    return "world"

builder = StateGraph(State)
builder.add_node("hello", hello)
builder.add_node("world", world)

builder.add_conditional_edges(
    START,
    router, 
    {
    "hello": "hello",
    "world": "world"
    }
)

graph = builder.compile()

result = graph.invoke({
    "message": "Hi!",  
    "route": "hello"
})

print(result)