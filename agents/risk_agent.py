"""Risk Assessment Agent - Monitors supply chain risks and provides disruption alerts."""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from config.settings import get_risk_model, get_model_temperature


RISK_SYSTEM_PROMPT = """You are a Supply Chain Risk Analyst specializing in identifying, assessing,
and mitigating supply chain vulnerabilities.

Your expertise includes:
- Risk identification and categorization (strategic, operational, tactical)
- Risk scoring and prioritization frameworks
- Business continuity planning (BCP)
- Scenario analysis and stress testing
- Geographic and geopolitical risk assessment
- Single-source dependency analysis
- Early warning indicators and monitoring

You help users proactively identify risks and develop mitigation strategies."""


@tool
def assess_risk(category: str | None = None, severity: str = "all") -> str:
    """Assess supply chain risks.

    Args:
        category: Risk category ("supply", "demand", "logistics", "financial", None for all)
        severity: Minimum severity filter ("critical", "high", "medium", "all")

    Returns:
        Risk assessment with scores and mitigation suggestions
    """
    risks = [
        {
            "id": "R-001",
            "category": "supply",
            "severity": "critical",
            "description": "Single source for SKU-004 (Gadget X)",
            "impact": "High",
            "likelihood": "High",
            "score": 9.0,
            "mitigation": "Qualify secondary supplier within 30 days",
        },
        {
            "id": "R-002",
            "category": "logistics",
            "severity": "high",
            "description": "Port congestion delays at West Coast ports",
            "impact": "Medium",
            "likelihood": "High",
            "score": 7.5,
            "mitigation": "Diversify entry ports; increase safety stock",
        },
        {
            "id": "R-003",
            "category": "financial",
            "severity": "medium",
            "description": "Supplier currency exposure (EUR/USD)",
            "impact": "Low",
            "likelihood": "Medium",
            "score": 5.0,
            "mitigation": "Hedge 50% of EUR exposure",
        },
        {
            "id": "R-004",
            "category": "demand",
            "severity": "high",
            "description": "Seasonal demand spike for Q4",
            "impact": "High",
            "likelihood": "High",
            "score": 8.0,
            "mitigation": "Pre-build inventory in Q3; plan logistics capacity",
        },
        {
            "id": "R-005",
            "category": "supply",
            "severity": "high",
            "description": "Supplier SUP-003 geopolitical risk",
            "impact": "High",
            "likelihood": "Medium",
            "score": 7.0,
            "mitigation": "Develop alternative EU supplier options",
        },
    ]

    # Filter by category and severity
    severity_order = {"critical": 0, "high": 1, "medium": 2, "all": 3}
    filtered = [
        r for r in risks
        if (category is None or r["category"] == category)
        and (severity == "all" or severity_order.get(r["severity"], 3) <= severity_order.get(severity, 3))
    ]

    result = f"Risk Assessment Report" + (f" - Category: {category}" if category else "") + "\n\n"

    for r in sorted(filtered, key=lambda x: x["score"], reverse=True):
        result += f"""[{r['severity'].upper()}] {r['id']}: {r['description']}
   Impact: {r['impact']} | Likelihood: {r['likelihood']} | Score: {r['score']}/10
   Mitigation: {r['mitigation']}

"""

    return result


@tool
def get_risk_alerts() -> str:
    """Get active risk alerts requiring attention.

    Returns:
        Current alerts with recommended actions
    """
    alerts = [
        {
            "level": "critical",
            "title": "Supply Disruption: Gadget X",
            "message": "Current supplier unable to meet demand. Stock critically low.",
            "action": "Immediate: Activate emergency procurement. Long-term: Qualify backup supplier.",
        },
        {
            "level": "warning",
            "title": "Logistics Capacity Concern",
            "message": "Q4 carrier capacity expected to be 80% committed by Oct 1.",
            "action": "Book shipments early; consider premium carrier for critical items.",
        },
        {
            "level": "info",
            "title": "Currency Exposure Update",
            "message": "EUR strengthened 3% vs USD. Monitoring impact on EuroParts orders.",
            "action": "Review pricing strategy for EU-sourced products.",
        },
    ]

    icon_map = {"critical": "🚨", "warning": "⚠️", "info": "ℹ️"}

    result = "Active Risk Alerts:\n\n"
    for alert in alerts:
        icon = icon_map.get(alert["level"], "")
        result += f"{icon} [{alert['level'].upper()}] {alert['title']}\n"
        result += f"   {alert['message']}\n"
        result += f"   Action: {alert['action']}\n\n"

    return result


@tool
def scenario_analysis(scenario_name: str) -> str:
    """Run scenario analysis for supply chain disruption.

    Args:
        scenario_name: Scenario to analyze:
            - "portClosure": West Coast port closure
            - "supplierFailure": Key supplier goes bankrupt
            - "demandSpike": Unexpected 50% demand increase
            - "rawMaterialShortage": Critical raw material shortage

    Returns:
        Impact analysis and recommended responses
    """
    scenarios = {
        "portClosure": {
            "description": "West Coast port closure for 2 weeks",
            "affected_skus": "SKU-001, SKU-003",
            "days_of_inventory": 12,
            "financial_impact": "$250K delayed revenue",
            "mitigation": "Diversify ports; pre-position inventory at East Coast",
        },
        "supplierFailure": {
            "description": "Key supplier (SUP-001) goes bankrupt",
            "affected_skus": "SKU-002, SKU-005",
            "days_of_inventory": 5,
            "financial_impact": "$500K potential loss",
            "mitigation": "Dual sourcing; supplier financial monitoring",
        },
        "demandSpike": {
            "description": "Unexpected 50% demand increase for Widget A",
            "affected_skus": "SKU-001",
            "days_of_inventory": 3,
            "financial_impact": "$100K incremental orders backlog",
            "mitigation": "Safety stock increase; capacity expansion agreement",
        },
        "rawMaterialShortage": {
            "description": "Global semiconductor shortage",
            "affected_skus": "SKU-001, SKU-002, SKU-004",
            "days_of_inventory": 8,
            "financial_impact": "$750K production impact",
            "mitigation": "Long-term contracts; buffer stock; material diversification",
        },
    }

    if scenario_name not in scenarios:
        available = ", ".join(scenarios.keys())
        return f"Unknown scenario. Available: {available}"

    s = scenarios[scenario_name]

    return f"""Scenario: {s['description']}

Impact Assessment:
- Affected Products: {s['affected_skus']}
- Days of Inventory: {s['days_of_inventory']}
- Financial Impact: {s['financial_impact']}

Recommended Actions:
1. {s['mitigation'].split(';')[0]}
2. {s['mitigation'].split(';')[1] if ';' in s['mitigation'] else 'Monitor situation daily'}

Business Continuity: Activate BCP protocols if scenario occurs"""


RISK_TOOLS = [assess_risk, get_risk_alerts, scenario_analysis]


def create_risk_agent(model_name: str | None = None, temperature: float | None = None):
    """Create the risk assessment agent."""
    model_name = model_name or get_risk_model()
    temperature = temperature if temperature is not None else get_model_temperature()
    model = ChatOpenAI(model=model_name, temperature=temperature)
    return create_agent(
        model=model,
        tools=RISK_TOOLS,
        system_prompt=RISK_SYSTEM_PROMPT,
    )