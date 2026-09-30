from typing import TypedDict,Annotated
from langgraph.graph import StateGraph, START, END 
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage

def add_step(a: int, b: int) -> int:    # 自定义一个函数，用于将step字段的值进行累加
    return a + b


class State(TypedDict):
    message: Annotated[list,add_messages]  # 使用Annotated来标记message字段为消息列表
    step: Annotated[int,add_step]  # 使用Annotated来标记step字段为消息列表

def hello(state: State):    # 这是一个抽象节点，用来模拟hello的行为，实际上可以是任意有逻辑的函数。
    print("hello收到", state)
    return {
        "message": [
            HumanMessage(content="Hello")
        ],
        "step":1
    }



builder = StateGraph(State)
builder.add_node("hello", hello)
builder.add_edge(START, "hello")
builder.add_edge("hello", END)
graph = builder.compile()

result = graph.invoke({
   "message": [
       HumanMessage(content="Hi!")
   ],
   "step": 1
})

print("最终结果：" + str(result))