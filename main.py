"""Main entry point for Supply Chain Multi-Agent System.

A LangGraph-based multi-agent orchestration system for supply chain management.
Uses the Subagents pattern where a main orchestrator coordinates specialized agents.
"""

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load environment variables (add your OPENAI_API_KEY to .env)
load_dotenv()

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from config.callbacks import RichTerminalCallbackHandler

console = Console()


def main():
    """Run the Supply Chain Multi-Agent System interactively."""
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment.")
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-key-here'  # Linux/Mac")
        print("  set OPENAI_API_KEY=your-key-here       # Windows")
        return

    # Import after env check
    from agents import create_orchestrator_agent

    print("=" * 60)
    print("Supply Chain Multi-Agent Orchestration System")
    print("=" * 60)
    print("""
This system coordinates specialized agents for supply chain management:

- Inventory Agent: Stock levels, reorder points
- Demand Agent: Forecasting and demand analysis
- Logistics Agent: Shipping and route optimization
- Supplier Agent: Vendor management
- Risk Agent: Risk assessment and monitoring

Type your query or 'quit' to exit.
""")

    # Create the orchestrator agent (uses OPENAI_MODEL from env)
    orchestrator = create_orchestrator_agent()

    # Interactive loop
    while True:
        try:
            user_input = console.input("\n[bold green]You:[/bold green] ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                console.print("[bold yellow]Goodbye![/bold yellow]")
                break

            if not user_input:
                continue

            # Invoke the orchestrator with a loading status
            with console.status("[bold cyan]Orchestrator is analyzing the task...[/bold cyan]", spinner="dots"):
                result = orchestrator.invoke({
                    "messages": [HumanMessage(content=user_input)]
                }, config={"callbacks": [RichTerminalCallbackHandler()]})

            # Print the response
            response = result["messages"][-1]
            console.print("\n[bold blue]Orchestrator:[/bold blue]")
            console.print(Markdown(response.content))

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def run_graph_mode():
    """Run using explicit LangGraph workflow (alternative to agent-based)."""
    from agents.orchestrator import create_supply_chain_graph

    print("Starting in Graph Mode...")
    graph = create_supply_chain_graph()

    result = graph.invoke({
        "messages": [HumanMessage(content="What's the current inventory status?")]
    })

    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()