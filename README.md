# Supply Chain Multi-Agent System

A **LangGraph-based multi-agent orchestration system** for supply chain management using the **Subagents pattern**.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUPPLY CHAIN ORCHESTRATOR                     │
│                    (Main Supervisor Agent)                        │
└─────────────────────────────────────────────────────────────────┘
                    │                    │                  │
        ┌───────────┴───┐    ┌──────────┴────┐   ┌────────┴────────┐
        │   INVENTORY   │    │    DEMAND    │   │   LOGISTICS   │
        │    AGENT      │    │    AGENT     │   │    AGENT      │
        └───────────────┘    └─────────────┘   └───────────────┘
        ┌───────────────┐    ┌─────────────┐   ┌───────────────┐
        │   SUPPLIER   │    │    RISK    │   │              │
        │    AGENT     │    │    AGENT   │   │              │
        └───────────────┘    └────────────┘   └───────────────┘
```

## Features

### Specialized Agents

1. **Inventory Manager Agent**
   - Check stock levels
   - Calculate EOQ (Economic Order Quantity)
   - Generate reorder recommendations
   - Inventory alerts

2. **Demand Forecaster Agent**
   - Demand forecasting with multiple methods
   - Seasonality analysis
   - Trend analysis

3. **Logistics Coordinator Agent**
   - Schedule shipments
   - Track deliveries
   - Route optimization
   - Shipping rate comparison

4. **Supplier Manager Agent**
   - Supplier information lookup
   - Vendor comparison
   - Risk evaluation

5. **Risk Assessor Agent**
   - Supply chain risk assessment
   - Active risk alerts
   - Scenario analysis

## Installation

```bash
# Clone or navigate to the project directory
cd supply_chain_multi_agent

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .

# Copy environment template
cp .env.example .env

# Add your OpenAI API key to .env
# OPENAI_API_KEY=your-key-here
```

## Usage

### Interactive Mode

```bash
python main.py
```

Example queries:
- "What's the current inventory status for SKU-001?"
- "Compare vendors for product SKU-002"
- "Generate a 12-month demand forecast for SKU-003"
- "What are the current risk alerts?"
- "Schedule a shipment from Chicago to New York"

### Programmatic Usage

```python
from agents import create_orchestrator_agent
from langchain_core.messages import HumanMessage

# Create the orchestrator
orchestrator = create_orchestrator_agent(model_name="gpt-4.1")

# Query the system
result = orchestrator.invoke({
    "messages": [HumanMessage(content="Check inventory alerts")]
})

print(result["messages"][-1].content)
```

### Using Subagents Directly

```python
from agents import (
    create_inventory_agent,
    create_demand_agent,
    create_supplier_agent,
)

# Use specific agents directly
inventory_agent = create_inventory_agent()
result = inventory_agent.invoke({
    "messages": [HumanMessage(content="What's low stock?")]
})
```

## Project Structure

```
supply_chain_multi_agent/
├── agents/
│   ├── __init__.py          # Agent exports
│   ├── orchestrator.py      # Main supervisor agent + graph
│   ├── inventory_agent.py   # Inventory management
│   ├── demand_agent.py      # Demand forecasting
│   ├── logistics_agent.py   # Logistics coordination
│   ├── supplier_agent.py    # Supplier management
│   └── risk_agent.py        # Risk assessment
├── tools/
│   ├── __init__.py          # Tool exports
│   └── supply_chain_tools.py # Cross-agent utilities
├── config/
│   └── agents.yaml          # Agent configurations
├── main.py                  # Entry point
├── pyproject.toml           # Project configuration
├── .env.example            # Environment template
└── README.md
```

## Design Patterns

This system uses the **Subagents pattern** from LangGraph:

- **Centralized Control**: All routing passes through the main orchestrator
- **Stateless Subagents**: Each subagent starts fresh with only relevant context
- **Tool-Based Invocation**: Subagents are wrapped as tools the main agent can call
- **Context Isolation**: Prevents context bloat by isolating complex tasks

## Customization

### Adding New Subagents

1. Create a new agent file in `agents/` (e.g., `production_agent.py`)
2. Define tools and system prompt
3. Register in `orchestrator.py`:
   ```python
   from .production_agent import create_production_agent, PRODUCTION_TOOLS
   SUBAGENTS["production"] = create_production_agent()
   ALL_TOOLS.extend(PRODUCTION_TOOLS)
   ```

### Adding Tools to Existing Agents

Add new `@tool` decorated functions to the respective agent file.

## License

MIT