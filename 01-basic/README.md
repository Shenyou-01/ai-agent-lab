# 01_basic_graph

## 学到什么

- State  
- Node
- Edge
- START / END
- compile()
- invoke()

## 核心理解

LangGraph 的基本执行流程：

State
↓
Node
↓
State Update
↓
Next Node

## 一个重要实验

hello 节点修改 message：

"Hi" → "Hi Hello"

world 节点收到：

{"message": "Hi Hello"}

说明前一个节点返回的 State 更新会成为后一个节点的输入。

## compile()

compile() 将构建好的 Graph 转换为可执行的 Graph 对象

compile() 本身不会执行 Node

真正执行发生在：

graph.invoke(...)