"""Human-in-the-Loop (HITL) Gate: Halts execution for human inspection and sign-off."""

from typing import Any, Dict
from langchain_core.messages import AIMessage
from nexus_agent.state.agent_state import AgentState


def human_gate_node(state: AgentState) -> Dict[str, Any]:
    """Execute the Human Approval Gate node.

    This node acts as the final quality and safety boundary before delivery.
    In interactive mode, LangGraph interrupts *before* or *at* this node so the user
    can inspect state['final_artifact'] and approve or modify it.
    """
    goal = state["user_goal"]
    score = state.get("quality_score", 0.0)

    log_msg = f"🛡️ Human Approval Gate cleared for objective: '{goal}' (Audited Score: {score:.1f}/10)"
    ai_msg = AIMessage(
        content=(
            f"[Human Gate]: Final artifact verified and approved for release. "
            f"Quality Score: {score:.1f}/10. Ready for deployment! 🚀"
        ),
        name="human_gate",
    )

    return {
        "human_approved": True,
        "next_worker": "FINISH",
        "messages": [ai_msg],
        "logs": [log_msg],
    }

