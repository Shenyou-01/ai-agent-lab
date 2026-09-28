# 02 Control Flow

## Concepts

- Conditional Edge
- Router
- Route Result
- Node
- Mapping

## 1. 为什么需要 Conditional Edge

普通 Edge：
A → B

只能固定走向。

Conditional Edge：
A → Router → B / C

可以根据 State 决定下一步。

## 2. Router 是什么

Router 本质上是一个用于“做路由判断”的函数。

State
 ↓
Router
 ↓
Route Result

Router 不负责真正执行业务。

## 3. Router 返回值 ≠ Node 名称

例如：

Router 返回：
"go_hello"

真正的 Node：
"hello"

通过映射关系：

"go_hello" → "hello"

所以：

Router 返回的是“选择结果”
Node 名称是“实际执行目标”

## 4. Conditional Edge

核心结构：

builder.add_conditional_edges(
    START,
    router,
    {
        "hello": "hello",
        "world": "world"
    }
)

其中：

START
→ 从哪里开始进行条件路由

router
→ 如何判断

mapping
→ 判断结果对应哪个 Node

## 5. 实验

route = "hello"

结果：

Hi! Hello

route = "world"

结果：

Hi! World

## 6. 踩坑记录

错误：

builder.add_edge(START, "router")

报错：

ValueError: Found edge ending at unknown node `router`

原因：

当前 router 只是 Conditional Edge 使用的路由函数，
并不是 Graph 中注册的 Node。

## 7. 我的理解

Conditional Edge 是一种条件路由机制。

Router 根据当前 State 做判断，
返回一个路由结果，
Conditional Edge 根据映射关系找到真正要执行的 Node。

## 8. Execution Flow

State
 ↓
Router
 ↓
Route Result
 ↓
Mapping
 ↓
Node
 ↓
State Update
 ↓
Next Node