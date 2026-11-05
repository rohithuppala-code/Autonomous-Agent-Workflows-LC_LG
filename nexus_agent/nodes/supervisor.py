"""Supervisor Agent Node: Hierarchical orchestrator and routing manager."""

from typing import Any, Dict
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from cogniflow.models.factory import get_chat_model
from nexus_agent.state.agent_state import AgentState


SUPERVISOR_SYSTEM_PROMPT = """You are the Executive Supervisor of NexusAgent OS.
Your responsibility:
1. Deconstruct the user's objective into a 3-stage strategic task plan.
2. Oversee progress across Researcher, Coder, and Critic specialists.
3. Determine the immediate next worker to advance the objective towards completion.
"""


def supervisor_node(state: AgentState) -> Dict[str, Any]:
    """Execute the Supervisor Agent node.

    Inspects state and decides:
    - Plan decomposition (if not already created)
    - Next worker assignment: 'researcher' | 'coder' | 'critic' | 'human_gate' | 'FINISH'
    """
    goal = state["user_goal"]
    task_plan = state.get("task_plan", [])
    research_done = bool(state.get("research_data", {}).get("status") == "completed")
    code_done = bool(state.get("code_solution", {}).get("status") == "completed")
    critic_done = bool(state.get("critic_review", {}).get("score"))
    quality_score = state.get("quality_score", 0.0)
    revision_count = state.get("revision_count", 0)
    max_revisions = state.get("max_revisions", 3)
    human_approved = state.get("human_approved", False)

    # 1. Generate task plan if empty
    if not task_plan:
        try:
            model = get_chat_model(temperature=0.2)
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", SUPERVISOR_SYSTEM_PROMPT),
                    (
                        "human",
                        "Objective: {goal}\n\n"
                        "Decompose this into 3 concise, numbered milestones.",
                    ),
                ]
            )
            chain = prompt | model | StrOutputParser()
            plan_text = chain.invoke({"goal": goal})
            task_plan = [line.strip() for line in plan_text.split("\n") if line.strip()][:3]
        except Exception:
            task_plan = [
                f"1. Gather factual intelligence for '{goal}'",
                "2. Synthesize modular technical implementation",
                "3. Perform quality audit & security review",
            ]

    # 2. Determine Next Worker based on deterministic state logic
    if not research_done:
        next_worker = "researcher"
        reason = "Dispatching to Researcher Specialist for fact-gathering."
    elif not code_done:
        next_worker = "coder"
        reason = "Dispatching to Coder Specialist for implementation."
    elif not critic_done or (quality_score < 8.0 and revision_count < max_revisions):
        next_worker = "critic"
        reason = "Dispatching to Critic Auditor for quality review."
    elif not human_approved:
        next_worker = "human_gate"
        reason = "All agent milestones passed! Pausing at Human Approval Gate."
    else:
        next_worker = "FINISH"
        reason = "Human approved deliverable. Workflow finalized."

    log_msg = f"👑 Supervisor designated next step: '{next_worker}' ({reason})"
    ai_msg = AIMessage(
        content=f"[Supervisor]: {reason} Next worker -> {next_worker}",
        name="supervisor",
    )

    return {
        "task_plan": task_plan,
        "next_worker": next_worker,
        "messages": [ai_msg],
        "logs": [log_msg],
    }
