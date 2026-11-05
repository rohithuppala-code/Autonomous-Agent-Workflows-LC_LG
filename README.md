# 🧠 Autonomous Agentic Workflows & Multi-Agent OS (LC_LG)

A progressive, end-to-end production repository designed to master modern LLM application development, agentic workflows, and multi-agent coordination using **LangChain** and **LangGraph**.

---

## 📚 Zero-to-Hero Story Guides (Start Here!)
- 🍳 **[LangChain Basics Explained Like a Story](LC_BASICS.md)**: Understand the Chef, Recipe Card, and Conveyor Belt in 5 minutes with 0 jargon.
- 🕸️ **[LangGraph Basics Explained Like a Story](LG_BASICS.md)**: Understand State Machines, Nodes, Cycles, and Human-in-the-Loop using the 5-Star Restaurant team.

---

## 🗺️ How NexusAgent OS Works: The Visual Lifecycle

> 💡 **How to read this diagram**: Follow the numbers from **1️⃣ START** to **7️⃣ DELIVERED**! Every card shows the **exact Python file** responsible for that step.

```mermaid
flowchart TD
    %% Theme-Safe High-Contrast Styling (100% readable in both GitHub Light & Dark mode)
    classDef startNode fill:#15803D,stroke:#166534,stroke-width:2px,color:#FFFFFF,font-weight:bold;
    classDef supervisorNode fill:#EEF2FF,stroke:#4F46E5,stroke-width:2px,color:#0F172A,font-weight:bold;
    classDef researcherNode fill:#E0F2FE,stroke:#0284C7,stroke-width:2px,color:#0F172A,font-weight:bold;
    classDef coderNode fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#0F172A,font-weight:bold;
    classDef criticNode fill:#FEE2E2,stroke:#DC2626,stroke-width:2px,color:#0F172A,font-weight:bold;
    classDef humanNode fill:#D1FAE5,stroke:#059669,stroke-width:2px,color:#0F172A,font-weight:bold;
    classDef decisionNode fill:#F1F5F9,stroke:#475569,stroke-width:2px,color:#0F172A,font-weight:bold;
    classDef finishNode fill:#0F172A,stroke:#000000,stroke-width:2px,color:#FFFFFF,font-weight:bold;
    classDef storageNode fill:#F8FAFC,stroke:#64748B,stroke-width:2px,color:#0F172A;

    START(["🟢 1. START HERE: User Objective"]):::startNode
    SUP["👑 2. SUPERVISOR (nexus_agent/nodes/supervisor.py)<br/>• Reads goal<br/>• Creates 3-milestone plan<br/>• Dispatches first specialist"]:::supervisorNode
    RES["🔍 3. RESEARCHER (nexus_agent/nodes/researcher.py)<br/>• Searches live web via DuckDuckGo<br/>• Gathers benchmarks & real-world facts"]:::researcherNode
    COD["💻 4. CODER (nexus_agent/nodes/coder.py)<br/>• Writes Python implementation<br/>• Patches bugs flagged by Critic"]:::coderNode
    CRT["🧐 5. CRITIC AUDITOR (nexus_agent/nodes/critic.py)<br/>• Audits code & facts<br/>• Grades quality from 1.0 to 10.0"]:::criticNode
    DEC{"⚖️ Router: Did quality pass?<br/>(nexus_agent/edges/router.py)"}:::decisionNode
    HGT["🛡️ 6. HUMAN APPROVAL GATE (nexus_agent/nodes/human_gate.py)<br/>• Pauses graph execution<br/>• Asks YOU: Approve or Reject?"]:::humanNode
    FINISH(["🏁 7. DELIVERED: Verified Artifact"]):::finishNode
    SAV[("📸 CHECKPOINT VAULT (nexus_agent/checkpoints/memory_saver.py)<br/>Saves state snapshot to SQLite for time-travel")]:::storageNode

    START --> SUP
    SUP -->|"Dispatches research task"| RES
    RES -->|"Hands off factual findings"| COD
    COD -->|"Submits code solution"| CRT
    CRT --> DEC

    %% Self-Correction Cycle Loop
    DEC -->|"❌ Score < 8.0: Self-Healing Loop (Retry)"| COD
    DEC -->|"✅ Score >= 8.0: Audit Passed"| HGT

    %% Human in the loop gate
    HGT -->|"Developer clicks Approve"| FINISH
    FINISH -.->|"Auto-persisted"| SAV
```

---

## 🗂️ File-to-Role Cheat Sheet (What File Does What?)

If you are browsing the code, here is exactly where each piece lives and what it does:

| Step | File Path | Architectural Role | Plain-English Job Description |
|:---:|---|---|---|
| **Whiteboard** | [`nexus_agent/state/agent_state.py`](nexus_agent/state/agent_state.py) | **Central State** | The shared whiteboard dictionary holding all messages, drafts, scores, and logs. |
| **Step 1** | [`nexus_agent/nodes/supervisor.py`](nexus_agent/nodes/supervisor.py) | **👑 Supervisor** | The team manager. Decomposes the user prompt into milestones and decides who works next. |
| **Step 2** | [`nexus_agent/nodes/researcher.py`](nexus_agent/nodes/researcher.py) | **🔍 Researcher** | Gathers live data from the internet using DuckDuckGo search and Wikipedia. |
| **Step 3** | [`nexus_agent/nodes/coder.py`](nexus_agent/nodes/coder.py) | **💻 Coder** | Writes modular Python code. When the critic finds a bug, the coder rewrites and fixes it. |
| **Step 4** | [`nexus_agent/nodes/critic.py`](nexus_agent/nodes/critic.py) | **🧐 Critic Auditor** | Inspects code and facts, searches for bugs, and assigns a strict score (1.0 to 10.0). |
| **Step 5** | [`nexus_agent/edges/router.py`](nexus_agent/edges/router.py) | **🚦 Dynamic Router** | The crossroad. If score < 8.0, it routes back to Coder. If score ≥ 8.0, it proceeds to Human Gate. |
| **Step 6** | [`nexus_agent/nodes/human_gate.py`](nexus_agent/nodes/human_gate.py) | **🛡️ Human Gate** | Interrupts the autonomous run to let a real human inspect and approve before release. |
| **Storage** | [`nexus_agent/checkpoints/memory_saver.py`](nexus_agent/checkpoints/memory_saver.py) | **📸 Checkpointer** | Saves state history to SQLite after every node for resume capability and time-travel. |
| **Assembly** | [`nexus_agent/graph/builder.py`](nexus_agent/graph/builder.py) | **🕸️ Graph Builder** | Connects all nodes, conditional edges, and compile settings into a runnable state machine. |
| **Terminal** | [`nexus_agent/cli.py`](nexus_agent/cli.py) | **🚀 Interactive UI** | Beautiful Rich terminal application to run goals and view live streaming agent events. |

---

## ⚡ Step-by-Step Example Scenario: "Build a Vector DB Benchmark"

Here is what happens behind the scenes when you submit a real request to the system:

```text
1. 👤 YOU TYPE: "Analyze Pinecone vs Chroma, write a benchmark script, and verify it."

2. 👑 SUPERVISOR NODE:
   - Decomposes the goal into 3 milestones:
     [1] Gather latency and indexing specs for Pinecone & Chroma.
     [2] Write a Python benchmark script measuring queries per second.
     [3] Audit code for syntax errors and edge cases.
   - Assigns next worker: "researcher".

3. 🔍 RESEARCHER NODE:
   - Searches DuckDuckGo for: "Pinecone vs Chroma benchmark latency specs".
   - Saves empirical metrics and findings onto the shared whiteboard.
   - Hands off to: "coder".

4. 💻 CODER NODE (Draft 1):
   - Synthesizes a Python benchmark script using the retrieved latency numbers.
   - Submits draft to the whiteboard.
   - Hands off to: "critic".

5. 🧐 CRITIC AUDITOR NODE:
   - Evaluates the draft.
   - ⚠️ FOUND AN ISSUE: "Line 14 tries to parse latency as a string instead of float!"
   - Score: 6.5 / 10.0 (Status: FAILED).
   - 🔄 TRIGGERS SELF-HEALING LOOP: Routes back to "coder" with the exact bug traceback!

6. 💻 CODER NODE (Draft 2 - Self-Correction):
   - Reads the critic's bug description.
   - Casts latency to float(latency_ms) and adds exception handling.
   - Submits patched code to the whiteboard.

7. 🧐 CRITIC AUDITOR NODE (Re-Audit):
   - All tests pass! No syntax errors, facts verified.
   - Score: 9.2 / 10.0 (Status: APPROVED ✅).
   - Hands off to: "human_gate".

8. 🛡️ HUMAN APPROVAL GATE:
   - The autonomous system PAUSES completely.
   - Your terminal displays:
     "Audited deliverable ready (Score 9.2/10). Approve for release? [Y/n]:"
   - You type: "Y".

9. 🏁 RESULT:
   - The state is saved to the SQLite checkpoint vault.
   - The final, verified, bug-free deliverable is published to your terminal!
```

---

## 🍳 Phase 1 Overview: `cogniflow/` (LangChain Core)

Before moving to multi-agent graphs, the repository includes **CogniFlow**, demonstrating foundational LangChain primitives:

```mermaid
flowchart LR
    classDef lcBox fill:#EEF2FF,stroke:#4F46E5,stroke-width:2px,color:#0F172A,font-weight:bold;
    classDef lcTool fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#0F172A,font-weight:bold;
    classDef lcOut fill:#D1FAE5,stroke:#059669,stroke-width:2px,color:#0F172A,font-weight:bold;

    U["👤 User Input"]:::lcBox --> P["📋 PromptTemplate<br/>(prompts/templates.py)"]:::lcBox
    P --> M["🧠 ModelFactory<br/>(models/factory.py)"]:::lcBox
    M <--> T["🛠️ Tools: Web Search & Safe Math<br/>(tools/web_search.py)"]:::lcTool
    M --> S["🍱 Pydantic Output<br/>(schemas/outputs.py)"]:::lcOut
    S --> C["🖥️ Rich Terminal CLI<br/>(cogniflow/cli.py)"]:::lcOut
```

- **Universal LLM Factory**: Hot-swap between Google Gemini, OpenAI, and Groq without rewriting code.
- **Pydantic Structured Extraction**: Clean, typed JSON data models instead of unpredictable raw text.
- **LCEL Declarative Pipelines**: Chaining with `|`, `RunnableParallel`, and `RunnablePassthrough`.
- **Conversational Memory**: Isolated chat history sessions via `RunnableWithMessageHistory`.

---

## 🚀 Quickstart

### 1. Environment Setup
```bash
conda activate genaienv
pip install -r requirements.txt
```

### 2. Environment Variables
Copy `.env.example` to `.env` and set your API keys:
```bash
cp .env.example .env
```
*(Supports Google Gemini free tier from [Google AI Studio](https://aistudio.google.com/), Groq, or OpenAI!)*

---

## 🎮 Running the Applications

### Run Phase 2: NexusAgent OS (LangGraph Multi-Agent Team)
```bash
python -m nexus_agent.cli
```
*Choose Option 1 to watch the autonomous team stream live, or Option 2 to test the Human Approval Gate!*

### Run Phase 1: CogniFlow CLI (LangChain)
```bash
python -m cogniflow.cli
```

---

## 🧪 Testing & Verification

Run the full automated test suite (21 unit tests covering both systems):
```bash
pytest -v tests/
```
All 21 unit tests verify schema validation, safe tools, memory isolation, individual agent nodes, and end-to-end LangGraph state machine execution!
