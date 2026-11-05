"""The central shared state (The Kitchen Whiteboard) for NexusAgent OS."""

import operator
from typing import Annotated, Any, Dict, List, Optional, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """The central state dictionary passed between all nodes in the LangGraph workflow.

    Each node reads what it needs, performs work, and returns only the fields
    it updates. LangGraph applies the appropriate reducer (e.g. add_messages
    for conversation history, operator.add for logs, or overwrite for atomic fields).
    """

    # Core message history using the add_messages reducer
    messages: Annotated[Sequence[BaseMessage], add_messages]

    # Goal and Task Planning
    user_goal: str
    task_plan: List[str]

    # Specialist Agent Outputs
    research_data: Dict[str, Any]
    code_solution: Dict[str, Any]
    critic_review: Dict[str, Any]

    # Quality Gate & Cyclic Revision Tracking
    quality_score: float
    revision_count: int
    max_revisions: int

    # Routing and Governance
    next_worker: str
    human_approved: bool
    final_artifact: Optional[str]

    # Execution telemetry log (appends via operator.add)
    logs: Annotated[List[str], operator.add]


def create_initial_state(user_goal: str, max_revisions: int = 3) -> AgentState:
    """Helper to initialize a clean AgentState for a new workflow run."""
    return {
        "messages": [],
        "user_goal": user_goal,
        "task_plan": [],
        "research_data": {},
        "code_solution": {},
        "critic_review": {},
        "quality_score": 0.0,
        "revision_count": 0,
        "max_revisions": max_revisions,
        "next_worker": "supervisor",
        "human_approved": False,
        "final_artifact": None,
        "logs": [f"🚀 Workflow initialized with goal: '{user_goal}'"],
    }

