# 03 State Management

本部分学习 LangGraph 中的 **State Management（状态管理）**。

在前两个阶段中：

```text
01 Graph Basics
    ↓
学习如何构建 Graph

02 Control Flow
    ↓
学习 Graph 如何决定下一步执行什么

03 State Management
    ↓
学习 Graph 中的数据如何保存、更新和管理
```

如果说 Control Flow 解决的是：

> **下一步做什么？**

那么 State Management 解决的是：

> **当前有什么数据？这些数据如何变化？如何合并？运行环境信息又应该放在哪里？**

---

# 1. Learning Goals

本部分主要学习：

* State Update
* Reducer
* Messages State
* Runtime Context

并建立以下核心理解：

```text
State
  ↓
Node
  ↓
Update
  ↓
Reducer
  ↓
New State
```

同时理解：

```text
State
→ Graph 运行过程中不断变化的数据

Context
→ 本次 Graph Run 的外部运行环境信息
```

---

# 2. State Management 的整体模型

一个 LangGraph 的运行过程可以抽象成：

```text
                 Graph Run
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
       Context                State
     运行环境信息             当前运行状态
          │                     │
          │              ┌──────┴──────┐
          │              ↓             ↓
          │          messages         step
          │
          └──────────────┬──────────────
                         ↓
                        Node
                         │
                         ↓
                       Update
                         │
                         ↓
                      Reducer
                         │
                         ↓
                     New State
                         │
                         ↓
                   Next Node
```

因此，State Management 并不是单独的一个 API，而是一套：

> **状态定义 → 状态更新 → 状态合并 → 状态传递 → 运行上下文管理**

的机制。

---

# 3. State Update

## 3.1 什么是 State Update？

Node 执行之后，可以返回一个 **State Update**。

例如：

```python
def hello(state: State):
    return {
        "message": state["message"] + " Hello"
    }
```

这里 Node 并没有返回完整 State，而只是返回：

```text
Update
└── message
    └── 新值
```

LangGraph 会将这个 Update 应用到当前 State。

因此可以理解为：

```text
State
  ↓
Node
  ↓
Update
  ↓
Graph 合并
  ↓
New State
```

---

## 3.2 为什么 Node 不需要返回完整 State？

假设 State：

```python
class State(TypedDict):
    message: str
    step: int
```

当前：

```python
{
    "message": "Hi",
    "step": 1
}
```

Node 只想修改 `message`：

```python
return {
    "message": "Hello"
}
```

那么：

```text
旧 State
├── message = Hi
└── step = 1

Update
└── message = Hello

        ↓

新 State
├── message = Hello
└── step = 1
```

因此：

> **Node 返回的是它想修改的部分，而不是必须重新构造整个 State。**

---

# 4. Reducer

## 4.1 Reducer 是什么？

Reducer 可以理解为：

> **State 某个字段的 Merge Strategy（合并策略）。**

默认情况下，一个字段收到新的值时，可以理解为：

```text
旧值
 ↓
新值覆盖
```

而设置 Reducer 后：

```text
旧值 + 新值
      ↓
   Reducer
      ↓
   合并结果
```

---

## 4.2 示例

例如：

```python
from typing import Annotated, TypedDict


def add_step(old: int, new: int) -> int:
    return old + new


class State(TypedDict):
    step: Annotated[int, add_step]
```

假设当前：

```text
step = 5
```

Node 返回：

```python
{
    "step": 1
}
```

LangGraph 会使用 Reducer：

```text
old = 5
new = 1

5 + 1
 ↓
6
```

最终：

```text
step = 6
```

---

## 4.3 Reducer 的核心模型

```text
Old Value
     +
New Value
     ↓
 Reducer
     ↓
Merged Value
```

所以：

> **Reducer 决定了一个 State 字段收到更新后应该如何合并。**

---

# 5. Messages State

Agent 系统中最重要的 State 类型之一就是：

```python
messages
```

典型定义：

```python
from typing import Annotated

from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
```

---

# 6. Message 不是普通字符串

LangChain 中的 Message 是结构化对象。

常见类型包括：

```text
HumanMessage
AIMessage
ToolMessage
```

例如：

```python
HumanMessage(content="你好")
```

不是简单的：

```python
"你好"
```

而是一个带有结构化信息的消息对象。

例如：

```text
HumanMessage
├── content
├── id
├── additional_kwargs
└── response_metadata
```

AI 消息也可能包含：

```text
AIMessage
├── content
├── tool_calls
└── metadata
```

因此 Agent 可以知道：

```text
谁说的？
说了什么？
有没有调用工具？
调用了什么工具？
工具返回了什么？
```

---

# 7. `add_messages`

对于：

```python
messages: Annotated[list, add_messages]
```

可以先简单理解为：

> **告诉 LangGraph：`messages` 字段不要简单覆盖，而是按照 Message 的规则进行合并。**

例如初始：

```text
messages
└── HumanMessage("hi")
```

Node 返回：

```text
AIMessage("你好，我是AI")
```

经过 `add_messages`：

```text
messages
├── HumanMessage("hi")
└── AIMessage("你好，我是AI")
```

整体流程：

```text
Old Messages
     +
New Messages
     ↓
 add_messages
     ↓
Merged Messages
```

需要注意：

`add_messages` 不只是普通的 `list.extend()`，它还能够处理结构化 Message 的 ID 等信息，因此更适合 Agent 消息状态管理。

---

# 8. Messages State 的意义

对于 Agent，可以把 `messages` 理解成：

> **Agent 的执行历史。**

例如：

```text
messages
│
├── HumanMessage
│     "帮我查天气"
│
├── AIMessage
│     tool_call
│
├── ToolMessage
│     "西安今天晴"
│
└── AIMessage
      "今天西安天气晴朗"
```

因此：

```text
messages
     ↓
保存发生过什么
```

而其他 State 字段可以保存：

```text
step
tool_result
route
task
```

也就是当前程序需要直接使用的运行数据。

---

# 9. Runtime Context

State 之外，还有一个重要概念：

**Runtime Context**

它解决的问题是：

> **本次 Graph 运行时的外部运行环境信息应该放在哪里？**

例如：

```text
user_id
session_id
model
权限
配置
外部依赖
```

---

# 10. State 与 Context

两者可以这样区分：

|           | State                     | Context               |
| --------- | ------------------------- | --------------------- |
| 作用        | Graph 当前运行状态              | 本次运行的外部环境             |
| 是否不断变化    | 通常会                       | 通常相对稳定                |
| 典型数据      | messages、step、tool_result | user_id、session_id、配置 |
| 来源        | Graph 执行过程中产生/更新          | Graph Run 外部提供        |
| Node 获取方式 | `state`                   | `runtime.context`     |

核心区别：

```text
State
→ “现在发生了什么？”

Context
→ “这次运行处于什么环境？”
```

---

# 11. Runtime Context 实验

Context 可以在 `graph.invoke()` 时传入。

例如：

```python
result = graph.invoke(
    {
        "messages": [
            HumanMessage(content="hi")
        ]
    },
    context={
        "user_id": "张三",
        "session_id": "abc123"
    }
)
```

Graph 定义：

```python
class Context(TypedDict):
    user_id: str
    session_id: str


builder = StateGraph(
    State,
    context_schema=Context
)
```

Node：

```python
def test_node(state: State, runtime):
    username = runtime.context["user_id"]
    session_id = runtime.context["session_id"]

    print(f"当前用户是: {username}")
    print(f"当前会话是: {session_id}")
```

执行结果：

```text
当前用户是: 张三
当前会话是: abc123
```

这验证了：

```text
graph.invoke()
      │
      ├── State
      │
      └── Context
             │
             ↓
           Node
             │
       runtime.context
```

---

# 12. Context 不等于 State

Runtime Context 实验中：

```python
context={
    "user_id": "张三",
    "session_id": "abc123"
}
```

最终 State 仍然只有：

```text
messages
└── HumanMessage("hi")
```

并不会自动变成：

```text
State
├── messages
├── user_id
└── session_id
```

这说明：

> **Context 可以被 Node 使用，但它本身不会因为被读取而自动进入 State。**

如果 Node 希望将某个 Context 信息写入 State，需要显式返回 State Update。

例如：

```python
return {
    "message": f"当前用户是 {user_id}"
}
```

---

# 13. State、Messages、Context 的关系

到这里，可以把三者放在一起理解：

```text
                 Graph Run
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
       Context                State
          │                     │
   运行环境信息            运行中的数据
          │                     │
          │                ┌────┴────┐
          │                ↓         ↓
          │            messages     step
          │
          └──────────────┬──────────────
                         ↓
                        Node
                         │
                         ↓
                       Update
                         │
                         ↓
                      Reducer
                         │
                         ↓
                     New State
```

---

# 14. State Management 四个核心模块

## 14.1 State Update

解决：

> **State 怎么修改？**

```text
State
 ↓
Node
 ↓
Update
 ↓
New State
```

---

## 14.2 Reducer

解决：

> **多个更新怎么合并？**

```text
Old Value + New Value
          ↓
       Reducer
          ↓
     Merged Value
```

---

## 14.3 Messages State

解决：

> **Agent 的消息历史怎么保存和管理？**

```text
HumanMessage
      ↓
AIMessage
      ↓
ToolMessage
      ↓
AIMessage
```

---

## 14.4 Runtime Context

解决：

> **运行环境信息放在哪里？**

```text
Context
├── user_id
├── session_id
└── configuration
```

Node 通过：

```python
runtime.context
```

访问。

---

# 15. 与 Control Flow 的联系

第二部分学习的是：

```text
Control Flow
```

主要回答：

> **下一步执行什么？**

第三部分学习的是：

```text
State Management
```

主要回答：

> **当前有什么数据？数据怎么变化？**

两者结合：

```text
                 State
                   ↓
                  Node
                   ↓
              State Update
                   ↓
                Reducer
                   ↓
               New State
                   ↓
                Router
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
        Node               END
          │
          └────── Loop ─────┘
```

因此：

```text
Control Flow
     +
State Management
     ↓
Stateful Workflow
```

这已经是 Agent 工作流的重要基础。

---

# 16. Key Understanding

本部分最重要的不是记住 API，而是建立以下模型：

### ① State

> **保存 Graph 当前运行状态。**

```text
State = 当前运行的数据
```

### ② State Update

> **Node 对 State 提出的修改。**

```text
Node → Update
```

### ③ Reducer

> **决定 State 字段如何合并更新。**

```text
Old + New → Reducer → Merged
```

### ④ Messages

> **保存 Agent 的结构化消息和执行历史。**

```text
Human → AI → Tool → AI
```

### ⑤ Context

> **提供本次 Graph Run 的外部运行环境。**

```text
Context = Runtime Environment
```

最终可以浓缩成：

```text
State
→ 当前发生了什么

Node
→ 做什么

Update
→ 修改什么

Reducer
→ 怎么合并

Messages
→ 发生过什么

Context
→ 在什么环境下运行
```

---

# 17. Learning Experiments

本部分通过四个实验验证核心概念：

```text
03-state-management/
│
├── 03_01_state_update.py
│
├── 03_02_reducer.py
│
├── 03_03_messages_state.py
│
├── 03_04_runtime_context.py
│
└── README.md
```

实验过程：

```text
State Update
     ↓
Reducer
     ↓
Messages State
     ↓
Runtime Context
```

每个实验都通过实际运行代码验证 LangGraph 的行为，而不是只依赖 API 文档。

---

# 18. Learning Method

本项目采用：

```text
Concept
   ↓
Code
   ↓
Experiment
   ↓
Question
   ↓
Understanding
   ↓
Documentation
   ↓
Commit
```

核心原则：

> **Don't just make it work. Understand why it works.**

---

# 19. Next

下一阶段进入：

```text
04 Tools
```

将开始研究 Agent 如何与外部工具交互：

```text
LLM
 ↓
Tool Call
 ↓
Tool
 ↓
Tool Result
 ↓
Messages / State
 ↓
LLM
```

届时，本阶段学习的：

* State
* Reducer
* Messages
* Context

以及上一阶段学习的：

* Conditional Edge
* Router
* Loop

都会开始真正组合起来。

这将从：

```text
学习 Graph
```

逐渐进入：

```text
构建 Agent Workflow
```
