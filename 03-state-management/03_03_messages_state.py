from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage , AIMessage ,ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# state -> update -> reducer
# LLM / Tool / Agent
  
class State(TypedDict):
    messages : Annotated[list,add_messages]

def ai_reply(state:State):
    print("这是AI节点")
    print("当前的State"+str(state['messages']))

    return {"messages":
            AIMessage(content="你好！我是AI")
    }
    


builder = StateGraph(State)
builder.add_node("ai",ai_reply)
builder.add_edge(START,"ai")
builder.add_edge("ai",END)

graph= builder.compile()
result = graph.invoke(
    {
        "messages":[
            HumanMessage(content="hi")
        ]
    }
)

print(str(result["messages"]))