from typing import TypedDict    # TypedDict 是用于定义langGraph中State 结构的工具
from langgraph.graph import StateGraph, START, END    # StateGraph是用于构建状态图的构建器

class State(TypedDict):
    message: str

builder = StateGraph(State)    # 创建一个状态图构建器实例

def hello(state: State) -> State:
    return {"message": state["message"] + "Hello!"}    # 定义一个状态函数，返回一个包含消息的字典
    # 将状态函数添加到状态图中

def world(state: State) -> State:
    print("world 收到的 state:", state)
    return {"message": state["message"] + "World!"}    # 定义一个状态函数，返回一个包含消息的字典
    # 将状态函数添加到状态图中

builder.add_node("hello", hello)    # 将状态函数添加到状态图中
builder.add_node("world", world)    # 将状态函数添加到状态图中

builder.add_edge(START, "hello")    # 将起始状态连接到hello状态
builder.add_edge("hello", "world")    # 将hello状态连接到world状态
builder.add_edge("world", END)    # 将world 状态连接到结束状态

graph = builder.compile()    # 编译状态图，生成可执行的状态图对象

result = graph.invoke({
    "message": "Hi!"
})
print(result)