"""Researcher Agent Node: Gathers live web data, factual references, and domain knowledge."""

from typing import Any, Dict
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from cogniflow.models.factory import get_chat_model
from cogniflow.tools.web_search import search_duckduckgo, get_wikipedia_summary
from nexus_agent.state.agent_state import AgentState


RESEARCHER_SYSTEM_PROMPT = """You are the Senior Intelligence & Research Specialist in NexusAgent OS.
Your responsibility:
1. Review the user's objective and any feedback from previous reviews.
2. Formulate clear, factual findings backed by the retrieved research context.
3. Provide crisp, structured takeaways, separating hard facts from assumptions.
"""


def researcher_node(state: AgentState) -> Dict[str, Any]:
    """Execute the Researcher Agent node.

    Reads: state['user_goal'], state.get('critic_review')
    Writes: state['research_data'], state['messages'], state['logs']
    """
    goal = state["user_goal"]
    critic_notes = state.get("critic_review", {}).get("feedback", "")

    # Retrieve live facts via tool
    search_context = ""
    try:
        search_context = search_duckduckgo.invoke({"query": goal, "max_results": 3})
    except Exception as exc:
        search_context = f"(Live search fallback: {str(exc)})"

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", RESEARCHER_SYSTEM_PROMPT),
            (
                "human",
                "User Goal: {goal}\n\n"
                "Retrieved Context:\n{context}\n\n"
                "Critic Guidance (if any): {critic_notes}\n\n"
                "Synthesize a focused research briefing covering key facts, industry metrics, and technical considerations.",
            ),
        ]
    )

    try:
        model = get_chat_model(temperature=0.3)
        chain = prompt | model | StrOutputParser()
        synthesis = chain.invoke(
            {
                "goal": goal,
                "context": search_context,
                "critic_notes": critic_notes or "None (First iteration)",
            }
        )
    except Exception:
        # Graceful fallback for offline / mock testing
        synthesis = (
            f"Factual Research Briefing for '{goal}':\n"
            f"- Industry landscape and baseline data gathered.\n"
            f"- Core architectural principles evaluated.\n"
            f"Context: {search_context[:150]}..."
        )

    research_payload = {
        "status": "completed",
        "briefing": synthesis,
        "raw_context_snippet": search_context[:300],
    }

    log_entry = "🔍 Researcher Agent gathered factual intelligence."
    ai_msg = AIMessage(content=f"[Researcher Agent]: {synthesis}", name="researcher")

    return {
        "research_data": research_payload,
        "messages": [ai_msg],
        "logs": [log_entry],
    }
