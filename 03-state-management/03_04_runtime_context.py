from typing import TypedDict , Annotated
from langgraph.graph import StateGraph , START , END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage , AIMessage , ToolMessage

class State(TypedDict):
    messages : Annotated[list,add_messages]

class Context(TypedDict):
    user_id: str
    session_id: str

def test_node(state:State,runtime):
    username = runtime.context["user_id"]
    session_id = runtime.context["session_id"]
    print(f"当前用户是: {username}")
    print(f"当前会话是: {session_id}")
    print("这是测试节点")
    return {
        "messages": [
            AIMessage(content=f"你好！{username}，你的会话ID是{session_id}")
        ]
    }

builder = StateGraph(State,context_schema=Context)
builder.add_node("test", test_node)
builder.add_edge(START, "test")
builder.add_edge("test", END)
graph = builder.compile()

result = graph.invoke(
    {
        "messages":[
            HumanMessage(content="hi")
        ]
    },
    context={
        "user_id": "张三",
        "session_id": "abc123"
    }
)

print(str(result["messages"]))