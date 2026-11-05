# 🧠 Autonomous Agentic Workflows & Multi-Agent OS (LC_LG)

A progressive, end-to-end production repository designed to master modern LLM application development, agentic workflows, and multi-agent coordination using **LangChain** and **LangGraph**.

---

## 📚 Zero-to-Hero Story Guides (Start Here!)
- 🍳 **[LangChain Basics Explained Like a Story](file:///c:/Users/sairo/OneDrive/Documents/LC_LG/LC_BASICS.md)**: Understand the Chef, Recipe Card, and Conveyor Belt in 5 minutes with 0 jargon.
- 🕸️ **[LangGraph Basics Explained Like a Story](file:///c:/Users/sairo/OneDrive/Documents/LC_LG/LG_BASICS.md)**: Understand State Machines, Nodes, Cycles, and Human-in-the-Loop using the 5-Star Restaurant team.

---

## 🏗️ Repository Architecture

This repository is structured in two progressive phases:

### 🔹 Phase 1: `cogniflow/` (LangChain Expression Language - LCEL)
- **Universal LLM Factory**: Hot-swappable providers (OpenAI, Google Gemini, Groq).
- **Structured Outputs**: Pydantic validation and schema extraction.
- **LCEL Architecture**: Declarative chains, `RunnablePassthrough`, `RunnableParallel`, and `RunnableLambda`.
- **Dynamic Tool Execution**: Tool bindings, duckduckgo search, and custom tools.
- **Conversational Memory**: State management and message history.

### 🔹 Phase 2: `nexus_agent/` (Autonomous Multi-Agent System with LangGraph)
- **State Machine Architecture**: Nodes, edges, conditional routing, and cycles.
- **Hierarchical Supervision**: Supervisor agent orchestrating specialized worker agents.
- **Durable Persistence**: SQLite/Postgres checkpointing and state time-travel.
- **Human-in-the-Loop (HITL)**: Interrupts and approval gates for critical actions.
- **Event Streaming**: Low-latency token streaming and graph execution telemetry.

---

## 🚀 Quickstart

### 1. Environment Setup
```bash
conda activate genaienv
pip install -r requirements.txt
```

### 2. Environment Variables
Copy `.env.example` to `.env` and configure your API keys:
```bash
cp .env.example .env
```
