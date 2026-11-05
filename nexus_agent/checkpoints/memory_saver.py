"""Checkpoint storage and state time-travel utilities."""

from typing import Any, Dict, List, Optional
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.base import BaseCheckpointSaver


def get_checkpointer(saver_type: str = "memory", db_path: Optional[str] = None) -> BaseCheckpointSaver:
    """Instantiate a durable or in-memory checkpointer for LangGraph state persistence.

    Args:
        saver_type: 'memory' for ultra-fast in-memory state, or 'sqlite' for durable local DB.
        db_path: Path to sqlite database file if using persistent storage.

    Returns:
        An instance of BaseCheckpointSaver.
    """
    if saver_type.lower() == "memory":
        return MemorySaver()
    elif saver_type.lower() == "sqlite":
        try:
            from langgraph.checkpoint.sqlite import SqliteSaver
            import sqlite3

            conn = sqlite3.connect(db_path or "nexus_checkpoints.sqlite", check_same_thread=False)
            return SqliteSaver(conn)
        except (ImportError, Exception):
            # Graceful fallback to MemorySaver if sqlite optional driver is not installed
            return MemorySaver()
    else:
        return MemorySaver()


def get_thread_state_history(
    checkpointer: BaseCheckpointSaver,
    thread_id: str,
) -> List[Dict[str, Any]]:
    """Retrieve historical snapshots of a thread's state for time-travel debugging."""
    config = {"configurable": {"thread_id": thread_id}}
    try:
        history = list(checkpointer.list(config))
        return [
            {
                "checkpoint_id": getattr(snap, "checkpoint_id", str(idx)),
                "values": getattr(snap, "checkpoint", {}).get("channel_values", {}),
            }
            for idx, snap in enumerate(history)
        ]
    except Exception:
        return []
