"""Tests for NexusAgent OS state schema and initialization."""

from nexus_agent.state.agent_state import AgentState, create_initial_state


def test_create_initial_state():
    state = create_initial_state(user_goal="Build a microservice", max_revisions=4)

    assert state["user_goal"] == "Build a microservice"
    assert state["max_revisions"] == 4
    assert state["revision_count"] == 0
    assert state["quality_score"] == 0.0
    assert state["human_approved"] is False
    assert state["next_worker"] == "supervisor"
    assert len(state["logs"]) == 1
    assert "microservice" in state["logs"][0]


def test_state_schema_types():
    state = create_initial_state(user_goal="Test Goal")
    assert isinstance(state["task_plan"], list)
    assert isinstance(state["research_data"], dict)
    assert isinstance(state["code_solution"], dict)
    assert isinstance(state["critic_review"], dict)

