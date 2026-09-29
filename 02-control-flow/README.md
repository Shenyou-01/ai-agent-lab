# 02 · Control Flow

本章主要学习 LangGraph 中的图控制流机制。

在完成 Graph Basics 后，进一步理解节点之间如何根据 State 和条件进行动态跳转，以及如何通过图结构实现循环执行。

---

## 学习内容

### 02_1 · Conditional Edge

学习 LangGraph 中的条件边（Conditional Edge）。

核心内容：

* Conditional Edge 的作用
* Router 的概念
* Router 与 Node 的区别
* Router 返回值（Route Result）
* Route Result 与实际 Node Name 的关系
* Mapping 映射机制
* `START` 作为条件路由起点
* 条件路由的基本执行流程

基本结构：

```text
START
  ↓
Router
  ├── hello
  └── world
```

---

### 02_2 · Loop Mechanism

学习如何利用 LangGraph 的图结构实现循环执行。

核心内容：

* Loop 的本质
* 图中的 Back Edge
* Conditional Edge 与 Loop 的结合
* Agent → Tool → Agent 的典型循环结构
* State 在循环中的持续更新
* Loop 的终止条件
* 无限循环产生的原因

典型结构：

```text
        ┌──────────────┐
        │              ↓
START → Agent → Router ───→ Tool
          │                 │
          │                 │
          └──→ END          └──→ Agent
```

核心理解：

> Conditional Edge 决定是否继续，Back Edge 决定如何返回。

---

## 学习目标

完成本章后，应能够理解：

```text
Node
 ↓
Edge
 ↓
Conditional Edge
 ↓
Router
 ↓
Loop
```

并能够从图结构的角度分析 LangGraph 的执行流程，而不是仅仅记忆 API。

---

## 文件结构

```text
02-control-flow/
├── README.md
├── 02_1_conditional_edge.py
└── 02_2_loop_mechanism.py
```

---

## 学习路线

```text
01 · Graph Basics
        ↓
02 · Control Flow
        ├── 02_1 · Conditional Edge
        └── 02_2 · Loop Mechanism
```

后续将在此基础上继续学习更复杂的 Agent 工作流与状态管理机制。
