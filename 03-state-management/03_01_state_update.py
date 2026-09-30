from typing import TypedDict
from langgraph.graph import StateGraph , START , END

class State(TypedDict):
    message: str
    step: int

def hello(state: State):
    print("hello收到", state)
    return {
        "message": state["message"] + " Hello"
    }
def world(state: State):
    print("world收到", state)
    return {
        "message": state["message"] + " World"
    }


builder = StateGraph(State)

builder.add_node("hello",hello)
builder.add_node("world",world)

builder.add_edge(START, "hello")
builder.add_edge("hello", "world") 
builder.add_edge("world", END)
graph = builder.compile()

result = graph.invoke({
    "message": "Hi!",
    "step": 1
})
print("最终结果：" + result["message"])

