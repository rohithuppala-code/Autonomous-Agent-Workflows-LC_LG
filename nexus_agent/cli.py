"""Interactive streaming CLI terminal for NexusAgent OS built with Rich."""

import sys
import uuid
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm

from nexus_agent.state.agent_state import create_initial_state
from nexus_agent.graph.builder import build_nexus_graph
from nexus_agent.checkpoints.memory_saver import get_checkpointer, get_thread_state_history

console = Console()


def show_nexus_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                     🕸️ NEXUSAGENT MULTI-AGENT OS                      ║
    ║       Autonomous Hierarchical State Machine powered by LangGraph      ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
    console.print(f"[bold magenta]{banner}[/bold magenta]")


def show_graph_topology():
    table = Table(title="🗺️ NexusAgent OS Graph State Machine Topology", show_header=True)
    table.add_column("Node", style="bold cyan")
    table.add_column("Type", style="yellow")
    table.add_column("Role & Capabilities", style="white")
    table.add_column("Transition Target", style="green")

    table.add_row("supervisor", "Orchestrator", "Decomposes goals, selects next specialist", "Conditional: researcher/coder/critic")
    table.add_row("researcher", "Specialist", "Searches web & gathers empirical sources", "coder")
    table.add_row("coder", "Specialist", "Synthesizes code & addresses prior bugs", "critic")
    table.add_row("critic", "Evaluator", "Audits quality (1-10) & triggers revision loops", "Conditional: coder/researcher/human_gate")
    table.add_row("human_gate", "HITL Gate", "Pauses for human inspection before final delivery", "END (Finish)")

    console.print(table)


def run_multi_agent_goal(hitl_enabled: bool = False):
    goal = Prompt.ask("\n[bold yellow]Enter high-level objective for NexusAgent OS[/bold yellow]")
    thread_id = f"nexus_{uuid.uuid4().hex[:8]}"
    checkpointer = get_checkpointer("memory")

    app = build_nexus_graph(
        checkpointer=checkpointer,
        interrupt_before_human=hitl_enabled,
    )
    initial_state = create_initial_state(user_goal=goal, max_revisions=2)
    config = {"configurable": {"thread_id": thread_id}}

    console.print(f"\n[bold green]🚀 Launching Multi-Agent State Machine (Thread ID: {thread_id})...[/bold green]\n")

    current_state = None
    # Stream node execution events
    for event in app.stream(initial_state, config=config):
        for node_name, node_output in event.items():
            console.print(f"[bold cyan]⚡ Executed Node:[/bold cyan] [bold yellow]{node_name.upper()}[/bold yellow]")

            # Display node specific highlights
            if "logs" in node_output and node_output["logs"]:
                console.print(f"  [dim white]{node_output['logs'][-1]}[/dim white]")

            if node_name == "critic" and "critic_review" in node_output:
                score = node_output["critic_review"].get("score", 0.0)
                status_color = "green" if score >= 8.0 else "yellow"
                console.print(f"  [{status_color}]Auditor Score: {score:.1f}/10.0[/{status_color}]")

            current_state = node_output

    # Check if graph interrupted at Human Gate
    state_snapshot = app.get_state(config)
    if state_snapshot.next:
        console.print(Panel(
            "[bold yellow]🛑 Execution PAUSED at Human Approval Gate[/bold yellow]\n\n"
            "The autonomous multi-agent team has completed research, code, and auditing.\n"
            "Review is required before final publication.",
            border_style="yellow",
        ))

        artifact = state_snapshot.values.get("final_artifact") or "Artifact synthesized."
        console.print(Panel(Markdown(artifact), title="📋 Proposed Final Artifact", border_style="cyan"))

        approved = Confirm.ask("\n[bold green]Do you approve this deliverable for release?[/bold green]", default=True)
        if approved:
            # Resume graph execution past the interrupt
            console.print("[bold green]Resuming workflow past Human Approval Gate...[/bold green]")
            for event in app.stream(None, config=config):
                for node_name, node_output in event.items():
                    console.print(f"[bold green]↳ Cleared:[/bold green] {node_name}")
            console.print(Panel("[bold green]✅ Artifact Published Successfully![/bold green]", border_style="green"))
        else:
            console.print("[bold red]Release rejected by human supervisor.[/bold red]")
    else:
        # Completed directly
        final_artifact = state_snapshot.values.get("final_artifact")
        if final_artifact:
            console.print(Panel(Markdown(final_artifact), title="🎯 Final Verified Deliverable", border_style="green"))
        else:
            console.print("[bold green]Workflow completed successfully.[/bold green]")


def inspect_checkpoints():
    thread_id = Prompt.ask("\n[bold yellow]Enter Thread ID to inspect[/bold yellow]")
    checkpointer = get_checkpointer("memory")
    history = get_thread_state_history(checkpointer, thread_id)

    if not history:
        console.print(f"[dim]No saved checkpoints found for thread '{thread_id}'. (Try running a workflow first!)[/dim]")
        return

    table = Table(title=f"📸 Checkpoint Snapshots for Thread {thread_id}", show_header=True)
    table.add_column("#", style="dim")
    table.add_column("Checkpoint ID")
    table.add_column("Quality Score")
    table.add_column("Active Worker")

    for i, snap in enumerate(history):
        vals = snap.get("values", {})
        score = f"{vals.get('quality_score', 0.0):.1f}"
        worker = vals.get("next_worker", "N/A")
        table.add_row(str(i + 1), snap["checkpoint_id"][:12], score, worker)

    console.print(table)


def main():
    show_nexus_banner()

    while True:
        console.print("\n[bold]Select an action for NexusAgent OS:[/bold]")
        console.print("  [1] 🤖 Run Autonomous Multi-Agent Goal (Full Team Stream)")
        console.print("  [2] 🛑 Run Goal with Human-in-the-Loop (HITL Approval Gate)")
        console.print("  [3] 🗺️ View Graph Architecture & Specialist Topology")
        console.print("  [4] 📸 Inspect State Persistence & Checkpoints")
        console.print("  [0] 🚪 Exit")

        choice = Prompt.ask("[bold magenta]Option[/bold magenta]", choices=["1", "2", "3", "4", "0"], default="1")

        if choice == "1":
            run_multi_agent_goal(hitl_enabled=False)
        elif choice == "2":
            run_multi_agent_goal(hitl_enabled=True)
        elif choice == "3":
            show_graph_topology()
        elif choice == "4":
            inspect_checkpoints()
        elif choice == "0":
            console.print("[green]NexusAgent OS terminated. Goodbye![/green]")
            sys.exit(0)


if __name__ == "__main__":
    main()
