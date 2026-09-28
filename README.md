# AI Agent Lab

> A hands-on learning laboratory for AI Agent development.

**AI · CS · Builder**

这是我的 AI Agent 学习与实践仓库。

我希望通过持续的代码实验、问题验证和项目实践，逐步建立从 **LLM 基础 → AI Workflow → Agent → RAG → MCP → Multi-Agent** 的系统认知与开发能力。

这里不追求简单复制教程，而更关注：

> **代码为什么这样运行？框架为什么这样设计？数据是如何流动的？**

---

## Learning Roadmap

```text
AI Agent Lab
│
├── 01-basic/              # LangGraph 基础
│   ├── State
│   ├── Node
│   ├── Edge
│   ├── START / END
│   ├── compile()
│   └── invoke()
│
├── 02-control-flow/       # Workflow 控制流
│   ├── Conditional Edge
│   ├── Router
│   ├── Branching
│   └── Loop
│
├── 03-state/              # 状态管理
│   ├── State
│   ├── Messages
│   ├── State Update
│   ├── Reducer
│   └── Runtime Context
│
├── 04-tools/              # Tool Calling
│   ├── Tool
│   ├── Tool Schema
│   ├── Tool Calling
│   └── Tool Result
│
├── 05-agent/              # Agent
│   ├── Agent Loop
│   ├── Decision Making
│   ├── Tool Use
│   └── Agent State
│
├── 06-rag-agent/          # RAG + Agent
│   ├── Document Loading
│   ├── Chunking
│   ├── Embedding
│   ├── Vector Store
│   ├── Retrieval
│   └── RAG Agent
│
├── 07-mini-agent/         # Mini-Agent
│   └── Integrated Practice
│
└── notes/                 # 原理理解与实验记录
```

---

## Learning Progress

| Stage | Topic        | Status    |
| ----- | ------------ | --------- |
| 01    | Graph Basics | Completed |
| 02    | Control Flow | Learning  |
| 03    | State        | Planned   |
| 04    | Tools        | Planned   |
| 05    | Agent        | Planned   |
| 06    | RAG Agent    | Planned   |
| 07    | Mini-Agent   | Planned   |

---

## Core Concepts

### LangChain

理解 LLM 应用中的基础组件与组合方式。

```text
Prompt
   ↓
Model
   ↓
Parser
   ↓
Runnable
```

重点理解：

* Runnable
* `invoke()`
* Prompt
* Model
* Output Parser
* Chain

---

### LangGraph

学习如何构建具有状态、分支和循环的 AI Workflow。

```text
        ┌──────────────┐
        │    State     │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │     Node     │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │     Edge     │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │  Next Node   │
        └──────────────┘
```

核心概念：

* State
* Node
* Edge
* Conditional Edge
* Router
* Loop
* Reducer
* Graph Execution

---

### Agent

理解 Agent 不只是调用大模型，而是一个能够根据当前状态进行决策，并持续执行的系统。

```text
State
  ↓
LLM
  ↓
Decision
  ↓
┌───────────────┐
│ Need Tool ?   │
└───────┬───────┘
        │
   ┌────┴────┐
   ↓         ↓
 Tool       Finish
   ↓
Update State
   ↓
   LLM
   ↑
   └────────── Loop
```

重点理解：

* Agent Loop
* Decision Making
* Tool Calling
* State Management
* Workflow Control

---

### RAG

理解 Agent 如何连接外部知识。

```text
Documents
    ↓
Chunking
    ↓
Embedding
    ↓
Vector Store
    ↓
Retrieval
    ↓
Context
    ↓
LLM
    ↓
Answer
```

进一步探索：

* Vector Database
* Embedding
* Retrieval
* Reranking
* Context Construction
* RAG Agent

---

### MCP

进一步探索模型与外部工具、数据和服务之间的标准化连接方式。

```text
                 ┌── Tool
                 │
LLM / Agent ── MCP ── Resource
                 │
                 └── Prompt
```

---

## Learning Method

这个仓库采用：

```text
Concept
   ↓
Code
```
