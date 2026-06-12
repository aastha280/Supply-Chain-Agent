"""Supplier Management Agent - Manages supplier relationships, lead times, and vendor performance."""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from config.settings import get_supplier_model, get_model_temperature


SUPPLIER_SYSTEM_PROMPT = """You are a Supplier Manager specializing in vendor relationships,
procurement optimization, and supplier performance evaluation.

Your expertise includes:
- Supplier selection and qualification criteria
- Performance scorecards (quality, delivery, cost, responsiveness)
- Lead time analysis and optimization
- Total Cost of Ownership (TCO) calculations
- Supplier risk assessment and mitigation
- Contract negotiation strategies
- Vendor Managed Inventory (VMI) programs

You help users make informed decisions about supplier selection and management."""


@tool
def get_supplier_info(supplier_id: str | None = None) -> str:
    """Get detailed information about suppliers.

    Args:
        supplier_id: Supplier ID (None for all suppliers)

    Returns:
        Supplier details including contact info, lead times, and ratings
    """
    suppliers = {
        "SUP-001": {
            "name": "Acme Components Ltd",
            "rating": 4.5,
            "lead_time": "7 days",
            "min_order": 100,
            "specialty": "Electronics",
            "location": "Shenzhen, China",
        },
        "SUP-002": {
            "name": "Midwest Manufacturing",
            "rating": 4.8,
            "lead_time": "3 days",
            "min_order": 50,
            "specialty": "Heavy Industry",
            "location": "Chicago, USA",
        },
        "SUP-003": {
            "name": "EuroParts GmbH",
            "rating": 4.2,
            "lead_time": "10 days",
            "min_order": 200,
            "specialty": "Precision Parts",
            "location": "Munich, Germany",
        },
    }

    if supplier_id:
        if supplier_id in suppliers:
            s = suppliers[supplier_id]
            return f"""Supplier: {s['name']} ({supplier_id})
Rating: {s['rating']}/5.0
Lead Time: {s['lead_time']}
Minimum Order: {s['min_order']} units
Specialty: {s['specialty']}
Location: {s['location']}"""
        return f"Supplier {supplier_id} not found"

    result = "Supplier Directory:\n\n"
    for sid, s in suppliers.items():
        result += f"{sid}: {s['name']} - Rating: {s['rating']}/5, Lead: {s['lead_time']}\n"

    return result


@tool
def compare_vendors(product_sku: str) -> str:
    """Compare vendor options for a specific product.

    Args:
        product_sku: Product SKU to compare vendors for

    Returns:
        Vendor comparison with prices, lead times, and total scores
    """
    import random

    vendors = [
        {
            "id": "SUP-001",
            "name": "Acme Components",
            "unit_price": 12.50,
            "lead_time": "7 days",
            "quality_score": 4.3,
            "on_time": 92,
            "total_score": 8.7,
        },
        {
            "id": "SUP-002",
            "name": "Midwest Manufacturing",
            "unit_price": 15.75,
            "lead_time": "3 days",
            "quality_score": 4.8,
            "on_time": 98,
            "total_score": 9.2,
        },
        {
            "id": "SUP-003",
            "name": "EuroParts GmbH",
            "unit_price": 11.00,
            "lead_time": "10 days",
            "quality_score": 4.5,
            "on_time": 88,
            "total_score": 8.1,
        },
    ]

    result = f"""Vendor Comparison for {product_sku}:

Vendor       | Unit Price | Lead Time | Quality | On-Time% | Score
-------------|------------|-----------|---------|----------|------
"""

    for v in vendors:
        result += f"{v['name']:12} | ${v['unit_price']:9.2f} | {v['lead_time']:9} | {v['quality_score']:.1f}/5  | {v['on_time']:6}%   | {v['total_score']:.1f}\n"

    result += """
Analysis:
- Best Price: EuroParts GmbH ($11.00/unit)
- Fastest Delivery: Midwest Manufacturing (3 days)
- Highest Quality: Midwest Manufacturing (4.8/5.0)
- Best Overall: Midwest Manufacturing (Score: 9.2)

Recommendation: For urgent orders, use Midwest Manufacturing.
For non-urgent bulk orders, consider EuroParts for cost savings."""

    return result


@tool
def evaluate_supplier_risk(supplier_id: str | None = None) -> str:
    """Evaluate supplier risk factors.

    Args:
        supplier_id: Supplier ID to evaluate (None for all)

    Returns:
        Risk assessment with flags and recommendations
    """
    risk_data = {
        "SUP-001": {
            "name": "Acme Components",
            "financial_risk": "low",
            "geopolitical_risk": "medium",
            "quality_risk": "low",
            "concentration_risk": "high",
            "overall": "medium",
        },
        "SUP-002": {
            "name": "Midwest Manufacturing",
            "financial_risk": "low",
            "geopolitical_risk": "low",
            "quality_risk": "low",
            "concentration_risk": "medium",
            "overall": "low",
        },
        "SUP-003": {
            "name": "EuroParts GmbH",
            "financial_risk": "medium",
            "geopolitical_risk": "high",
            "quality_risk": "low",
            "concentration_risk": "high",
            "overall": "high",
        },
    }

    if supplier_id:
        if supplier_id in risk_data:
            r = risk_data[supplier_id]
            return f"""Risk Assessment: {r['name']} ({supplier_id})

Financial Risk: {r['financial_risk'].upper()}
Geopolitical Risk: {r['geopolitical_risk'].upper()}
Quality Risk: {r['quality_risk'].upper()}
Concentration Risk: {r['concentration_risk'].upper()}

Overall Risk: {r['overall'].upper()}
{"⚠️ Consider diversifying suppliers" if r['overall'] == 'high' else "✓ Risk levels acceptable"}"""
        return f"Supplier {supplier_id} not found"

    result = "Supplier Risk Summary:\n\n"
    result += "Supplier      | Financial | Geo | Quality | Conc. | Overall\n"
    result += "--------------|-----------|-----|---------|-------|--------\n"

    for sid, r in risk_data.items():
        result += f"{r['name']:13} | {r['financial_risk']:9} | {r['geopolitical_risk'][0].upper():3} | {r['quality_risk']:7} | {r['concentration_risk'][0].upper():5} | {r['overall'].upper()}\n"

    result += "\nFlags: H=High, M=Medium, L=Low"
    result += "\n\nRecommendation: Increase sourcing from SUP-002, evaluate alternatives for SUP-003"

    return result


SUPPLIER_TOOLS = [get_supplier_info, compare_vendors, evaluate_supplier_risk]


def create_supplier_agent(model_name: str | None = None, temperature: float | None = None):
    """Create the supplier management agent."""
    model_name = model_name or get_supplier_model()
    temperature = temperature if temperature is not None else get_model_temperature()
    model = ChatOpenAI(model=model_name, temperature=temperature)
    return create_agent(
        model=model,
        tools=SUPPLIER_TOOLS,
        system_prompt=SUPPLIER_SYSTEM_PROMPT,
    )