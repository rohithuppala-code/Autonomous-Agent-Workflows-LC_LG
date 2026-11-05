"""Tests for NexusAgent OS StateGraph compilation and end-to-end execution."""

from nexus_agent.state.agent_state import create_initial_state
from nexus_agent.graph.builder import build_nexus_graph
from nexus_agent.checkpoints.memory_saver import get_checkpointer


def test_graph_compilation():
    graph = build_nexus_graph()
    assert graph is not None


def test_end_to_end_graph_execution():
    checkpointer = get_checkpointer("memory")
    app = build_nexus_graph(checkpointer=checkpointer, interrupt_before_human=False)

    initial_state = create_initial_state(user_goal="Generate a prime number sieve in Python")
    config = {"configurable": {"thread_id": "test_thread_001"}}

    # Invoke complete graph
    final_state = app.invoke(initial_state, config=config)

    assert final_state is not None
    assert final_state["human_approved"] is True
    assert final_state["quality_score"] >= 1.0
    assert final_state["final_artifact"] is not None
    assert "prime number sieve" in final_state["final_artifact"].lower()

    # Verify checkpointer recorded the state
    saved_snapshot = app.get_state(config)
    assert saved_snapshot.values["human_approved"] is True

