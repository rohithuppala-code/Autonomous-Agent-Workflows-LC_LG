"""Tests for NexusAgent individual agent node functions."""

from nexus_agent.state.agent_state import create_initial_state
from nexus_agent.nodes.supervisor import supervisor_node
from nexus_agent.nodes.researcher import researcher_node
from nexus_agent.nodes.coder import coder_node
from nexus_agent.nodes.critic import critic_node
from nexus_agent.nodes.human_gate import human_gate_node


def test_supervisor_node_initial_dispatch():
    state = create_initial_state(user_goal="Create a sentiment analysis API")
    output = supervisor_node(state)

    assert "next_worker" in output
    assert output["next_worker"] == "researcher"
    assert len(output["task_plan"]) == 3
    assert len(output["messages"]) == 1


def test_researcher_node_execution():
    state = create_initial_state(user_goal="Explain Transformer attention mechanism")
    output = researcher_node(state)

    assert "research_data" in output
    assert output["research_data"]["status"] == "completed"
    assert "briefing" in output["research_data"]
    assert len(output["messages"]) == 1


def test_coder_node_execution():
    state = create_initial_state(user_goal="Implement binary search in Python")
    state["research_data"] = {"briefing": "Binary search divides array by half."}
    output = coder_node(state)

    assert "code_solution" in output
    assert output["code_solution"]["status"] == "completed"
    assert len(output["messages"]) == 1


def test_critic_node_evaluation():
    state = create_initial_state(user_goal="Write a fast sorting function")
    state["research_data"] = {"briefing": "Quicksort has average O(N log N)."}
    state["code_solution"] = {"implementation": "def quicksort(arr): return sorted(arr)"}
    output = critic_node(state)

    assert "critic_review" in output
    assert "quality_score" in output
    assert 1.0 <= output["quality_score"] <= 10.0
    assert len(output["messages"]) == 1


def test_human_gate_node_approval():
    state = create_initial_state(user_goal="Deploy to production")
    state["quality_score"] = 9.2
    output = human_gate_node(state)

    assert output["human_approved"] is True
    assert output["next_worker"] == "FINISH"

