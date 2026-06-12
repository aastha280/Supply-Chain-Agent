import os
import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Literal

# CopilotKit integration - use LangGraphAGUIAgent instead of deprecation LangGraphAgent
from copilotkit import CopilotKitSDK, LangGraphAGUIAgent
from copilotkit.integrations.fastapi import add_fastapi_endpoint

from agents.inventory_agent import create_inventory_agent
from agents.demand_agent import create_demand_agent
from agents.logistics_agent import create_logistics_agent
from agents.supplier_agent import create_supplier_agent
from agents.risk_agent import create_risk_agent
from config.settings import get_model_name

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is required. Add it to your .env file.")

SUBAGENTS = {
    "inventory": create_inventory_agent(),
    "demand":    create_demand_agent(),
    "logistics": create_logistics_agent(),
    "supplier":  create_supplier_agent(),
    "risk":      create_risk_agent(),
}

SYSTEM_PROMPT = """You are the Supply Chain Orchestrator — a senior supervisor coordinating
a team of specialized sub-agents. Delegate tasks using the task_dispatcher tool.
Always synthesize results from multiple agents into a clear markdown response."""

@tool
def task_dispatcher(
    agent_name: Literal["inventory", "demand", "logistics", "supplier", "risk"],
    task: str,
) -> str:
    """Delegate tasks to specialized supply chain sub-agents."""
    agent = SUBAGENTS[agent_name]
    result = agent.invoke({"messages": [HumanMessage(content=task)]})
    return result["messages"][-1].content

def build_graph():
    llm = ChatOpenAI(model=get_model_name(), temperature=0)
    llm_with_tools = llm.bind_tools([task_dispatcher])

    def call_model(state: MessagesState):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + state["messages"]
        return {"messages": [llm_with_tools.invoke(messages)]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode([task_dispatcher]))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    return graph.compile()

supply_chain_graph = build_graph()

from copilotkit import CopilotKitRemoteEndpoint, LangGraphAGUIAgent

# Initialize the CopilotKit endpoint properly
sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAGUIAgent(
            name="supply_chain_orchestrator",
            description="Multi-agent supply chain assistant.",
            graph=supply_chain_graph,
        )
    ]
)

# --- Monkeypatch sdk.info to bypass buggy dict_repr in 0.1.86 ---
import types
def safe_info(self, context=None):
    return {
        "actions": [],
        "sdkVersion": "0.1.86",
        "agents": [
            {
                "name": "supply_chain_orchestrator",
                "description": "Multi-agent supply chain assistant.",
                "type": "langgraph_agui",
            }
        ]
    }
sdk.info = types.MethodType(safe_info, sdk)
# ----------------------------------------------------------------

app = FastAPI(title="Supply Chain Control Tower")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_fastapi_endpoint(app, sdk, "/api/copilotkit")

if __name__ == "__main__":
    print("Server running at http://localhost:8000")
    print("CopilotKit endpoint at http://localhost:8000/api/copilotkit")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
