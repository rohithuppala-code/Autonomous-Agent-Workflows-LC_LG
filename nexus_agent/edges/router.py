"""Router functions for conditional transitions in the LangGraph state machine."""

from typing import Literal
from langgraph.graph import END
from nexus_agent.state.agent_state import AgentState


def supervisor_router(
    state: AgentState,
) -> Literal["researcher", "coder", "critic", "human_gate", "__end__"]:
    """Route from the Supervisor node to the appropriate specialist worker."""
    next_worker = state.get("next_worker", "researcher")

    if next_worker == "researcher":
        return "researcher"
    elif next_worker == "coder":
        return "coder"
    elif next_worker == "critic":
        return "critic"
    elif next_worker == "human_gate":
        return "human_gate"
    else:
        return END


def critic_router(
    state: AgentState,
) -> Literal["coder", "researcher", "human_gate", "__end__"]:
    """Determine whether to proceed to the Human Approval Gate or cycle back for revision.

    This implements the core self-healing / self-correction loop in LangGraph.
    """
    review = state.get("critic_review", {})
    is_approved = review.get("approved", False)
    score = state.get("quality_score", 0.0)
    revision_count = state.get("revision_count", 0)
    max_revisions = state.get("max_revisions", 3)

    # 1. Quality threshold satisfied OR safety cutoff reached -> advance to Human Gate
    if is_approved or score >= 8.0 or revision_count >= max_revisions:
        return "human_gate"

    # 2. Self-healing cycle: route back to the appropriate specialist
    critical_issues = review.get("critical_issues", [])
    issues_text = " ".join(critical_issues).lower()

    if "fact" in issues_text or "source" in issues_text or "information" in issues_text:
        return "researcher"
    else:
        # Default back to coder to patch implementation bugs
        return "coder"
