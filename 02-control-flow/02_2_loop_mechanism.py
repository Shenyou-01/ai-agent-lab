from typing import TypedDict
from langgraph.graph import StateGraph , START , END

class State(TypedDict):
    message: str
    route: str
    step: int   # 加入了step字段，用来记录循环的次数。

def tool(state: State):     # 这是一个抽象节点，用来模拟tool的行为。
    return {
        "message": state["message"] + " Hello I'm tool."
    }


def agent(state: State):    # 这是一个抽象节点，用来模拟agent的行为，实际上可以是任意有逻辑的函数。
    return {
        "message": state["message"] + "agent is here.",
        "step": state["step"] + 1
    }

def router(state:State):    # 目前这个路由选择器就成为了我们循环的核心，给出是结束还是继续循环的选择
    if END in state["route"] or state["step"] >= 10:
        return END
    return "tool"


builder = StateGraph(State)

builder.add_node("agent",agent)
builder.add_node("tool", tool)

builder.add_conditional_edges(      # 条件路由边由循环起始节点开始，通过路由器将其进行转发，决定是继续执行还是结束循环。 
    "agent",
    router, 
    {
    END: END,
    "tool": "tool"
    }
)

builder.add_edge(START, "agent")
builder.add_edge("tool", "agent")   # 这里的边是循环的关键，tool节点执行完后会返回到agent节点，形成一个循环。

graph = builder.compile()

result = graph.invoke({
    "message": "Hi!",  
    "route": "tool",
    "step": 0   # 初始化step为0，表示循环开始时的次数为0。
})

print(result)