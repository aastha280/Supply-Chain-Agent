"""Supply Chain Orchestrator - Main supervisor agent that coordinates sub-agents."""

from typing import Literal
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

from rich.console import Console
console = Console()

from .inventory_agent import create_inventory_agent, INVENTORY_TOOLS
from .demand_agent import create_demand_agent, DEMAND_TOOLS
from .logistics_agent import create_logistics_agent, LOGISTICS_TOOLS
from .supplier_agent import create_supplier_agent, SUPPLIER_TOOLS
from .risk_agent import create_risk_agent, RISK_TOOLS
from config.settings import get_model_name, get_model_temperature


# =============================================================================
# Sub-agent Registry (Single dispatch tool pattern)
# =============================================================================

SUBAGENTS = {
    "inventory": create_inventory_agent(),
    "demand": create_demand_agent(),
    "logistics": create_logistics_agent(),
    "supplier": create_supplier_agent(),
    "risk": create_risk_agent(),
}


@tool
def task_dispatcher(
    agent_name: Literal["inventory", "demand", "logistics", "supplier", "risk"],
    task: str,
) -> str:
    """Dispatch a task to a specialized supply chain sub-agent.

    Available agents:
    - inventory: Stock levels, reorder points, inventory optimization
    - demand: Demand forecasting and trend analysis
    - logistics: Shipping schedules and route optimization
    - supplier: Supplier relationships and vendor performance
    - risk: Risk assessment and disruption monitoring
    """
    console.print(f"\n[bold magenta]>> Orchestrating to [cyan]{agent_name}[/cyan] agent...[/bold magenta]")
    
    agent = SUBAGENTS[agent_name]
    result = agent.invoke({
        "messages": [HumanMessage(content=task)]
    })
    
    console.print(f"[bold green]>> [/bold green][cyan]{agent_name}[/cyan] agent completed task.")
    return result["messages"][-1].content


DISPATCH_TOOL = task_dispatcher
# The Orchestrator should ONLY have the dispatch tool so it delegates 
# rather than trying to use sub-agent tools directly itself.
ALL_TOOLS = [DISPATCH_TOOL]


# =============================================================================
# Orchestrator Agent Definition
# =============================================================================

SUPPLY_CHAIN_AGENT_DESCRIPTION = """You are the Supply Chain Orchestrator, a senior supervisor coordinating
a team of specialized agents to manage complex supply chain operations.

Your sub-agents:
- **inventory**: Manages stock levels, reorder points, and inventory optimization
- **demand**: Analyzes historical data and predicts future demand patterns
- **logistics**: Handles shipping, route optimization, and delivery tracking
- **supplier**: Manages supplier relationships and vendor performance
- **risk**: Monitors supply chain risks and provides disruption alerts

When to use each agent:
- User asks about current stock levels or needs reorder recommendations → inventory
- User wants demand predictions or trend analysis → demand
- User asks about shipments or delivery schedules → logistics
- User asks about supplier performance or comparisons → supplier
- User asks about risks or disruption scenarios → risk

You can also call multiple sub-agents in parallel for complex queries that require
coordinated analysis from multiple domains."""


def create_orchestrator_agent(model_name: str | None = None, temperature: float | None = None):
    """Create the main orchestrator/supervisor agent.

    Args:
        model_name: Model to use (defaults to OPENAI_MODEL env var)
        temperature: Model temperature (defaults to OPENAI_TEMPERATURE env var)
    """
    model_name = model_name or get_model_name()
    temperature = temperature if temperature is not None else get_model_temperature()

    model = ChatOpenAI(model=model_name, temperature=temperature)

    # Create the agent with all tools available
    from langchain.agents import create_agent

    agent = create_agent(
        model=model,
        tools=ALL_TOOLS,
        system_prompt=SUPPLY_CHAIN_AGENT_DESCRIPTION,
    )

    return agent


# =============================================================================
# LangGraph Workflow (Alternative approach with explicit graph)
# =============================================================================

from copilotkit import CopilotKitState

class SupplyChainState(CopilotKitState):
    """Extended state for supply chain orchestration."""
    task_type: str | None = None
    results: dict | None = None


def create_supply_chain_graph(model_name: str | None = None):
    """Create an explicit LangGraph workflow for supply chain management.

    This provides more control over the orchestration flow compared to
    the agent-based approach.
    """
    from langgraph.graph import StateGraph

    # Define model - use env var if not specified
    model_name = model_name or get_model_name()
    model = ChatOpenAI(model=model_name, temperature=0)

    # Define nodes
    def supervisor_node(state: SupplyChainState) -> AIMessage:
        """Supervisor decides which sub-agents to invoke."""
        # Build system prompt with available agents
        system_msg = SUPPLY_CHAIN_AGENT_DESCRIPTION + "\n\nUse the task_dispatcher tool to delegate work."

        response = model.bind_tools(
            ALL_TOOLS,
            system_message=system_msg
        ).invoke(state["messages"])

        return {"messages": [response]}

    # Build graph
    workflow = StateGraph(SupplyChainState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("inventory", create_inventory_agent())
    workflow.add_node("demand", create_demand_agent())
    workflow.add_node("logistics", create_logistics_agent())
    workflow.add_node("supplier", create_supplier_agent())
    workflow.add_node("risk", create_risk_agent())

    workflow.add_edge(START, "supervisor")
    workflow.add_edge("supervisor", END)

    return workflow.compile()