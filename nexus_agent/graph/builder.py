"""Constructs and compiles the NexusAgent OS hierarchical multi-agent state graph."""

from typing import List, Optional
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from nexus_agent.state.agent_state import AgentState
from nexus_agent.nodes.supervisor import supervisor_node
from nexus_agent.nodes.researcher import researcher_node
from nexus_agent.nodes.coder import coder_node
from nexus_agent.nodes.critic import critic_node
from nexus_agent.nodes.human_gate import human_gate_node
from nexus_agent.edges.router import supervisor_router, critic_router
from nexus_agent.checkpoints.memory_saver import get_checkpointer


def build_nexus_graph(
    checkpointer: Optional[BaseCheckpointSaver] = None,
    interrupt_before_human: bool = False,
) -> CompiledStateGraph:
    """Build, wire, and compile the full NexusAgent StateGraph.

    Architecture:
                     [START]
                        │
                        ▼
                  ┌────────────┐
                  │ Supervisor │◄────────────────┐
                  └─────┬──────┘                 │
                        │ (Conditional Edge)     │
                        ├─────────────┐          │
                        ▼             ▼          │
                 ┌────────────┐  ┌──────────┐    │
                 │ Researcher │  │  Coder   │◄───┤ (Self-Correction Loop)
                 └──────┬─────┘  └────┬─────┘    │
                        │             │          │
                        └────────►┌───▼──┐       │
                                  │Critic│───────┘
                                  └───┬──┘
                                      │ (Score >= 8.0)
                                      ▼
                               ┌──────────────┐
                               │  Human Gate  │ (Optional HITL Interrupt)
                               └──────┬───────┘
                                      │
                                      ▼
                                    [END]
    """
    workflow = StateGraph(AgentState)

    # 1. Register all specialized nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("human_gate", human_gate_node)

    # 2. Set the initial entrypoint
    workflow.set_entry_point("supervisor")

    # 3. Add Supervisor conditional dispatch edges
    workflow.add_conditional_edges(
        "supervisor",
        supervisor_router,
        {
            "researcher": "researcher",
            "coder": "coder",
            "critic": "critic",
            "human_gate": "human_gate",
            END: END,
        },
    )

    # 4. Standard linear specialist pipeline
    workflow.add_edge("researcher", "coder")
    workflow.add_edge("coder", "critic")

    # 5. Add Critic evaluation & cyclic self-correction edges
    workflow.add_conditional_edges(
        "critic",
        critic_router,
        {
            "coder": "coder",
            "researcher": "researcher",
            "human_gate": "human_gate",
            END: END,
        },
    )

    # 6. Terminal edge from Human Approval Gate
    workflow.add_edge("human_gate", END)

    # 7. Setup checkpointer & HITL interrupts
    cp = checkpointer or get_checkpointer("memory")
    interrupts: List[str] = ["human_gate"] if interrupt_before_human else []

    return workflow.compile(
        checkpointer=cp,
        interrupt_before=interrupts if interrupts else None,
    )

