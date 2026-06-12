"""Inventory Management Agent - Manages stock levels, reorder points, and inventory optimization."""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from config.settings import get_inventory_model, get_model_temperature


INVENTORY_SYSTEM_PROMPT = """You are an Inventory Manager specializing in stock level optimization,
reorder point calculation, and inventory analytics.

Your expertise includes:
- Economic Order Quantity (EOQ) calculations
- Safety stock determination based on service level targets
- ABC analysis for inventory classification
- Reorder point formulas: ROP = Lead Time × Daily Demand + Safety Stock
- Dead stock identification and liquidation recommendations

You have access to tools for checking stock levels and generating reorder recommendations."""


@tool
def check_stock_levels(product_sku: str | None = None, location: str | None = None) -> str:
    """Check current stock levels for products.

    Args:
        product_sku: Specific product SKU to check (optional - if None, returns all)
        location: Warehouse/location to check (optional)

    Returns:
        Stock level information including quantity on hand, reorder status
    """
    # Simulated inventory data - in production, connect to ERP/WMS
    inventory_data = {
        "SKU-001": {"name": "Widget A", "qty": 150, "reorder_point": 100, "status": "adequate"},
        "SKU-002": {"name": "Widget B", "qty": 45, "reorder_point": 50, "status": "low"},
        "SKU-003": {"name": "Widget C", "qty": 200, "reorder_point": 75, "status": "adequate"},
        "SKU-004": {"name": "Gadget X", "qty": 20, "reorder_point": 30, "status": "critical"},
        "SKU-005": {"name": "Gadget Y", "qty": 0, "reorder_point": 25, "status": "out_of_stock"},
    }

    if product_sku:
        data = inventory_data.get(product_sku, {"name": "Unknown", "qty": 0, "status": "not_found"})
        return f"Product {product_sku} ({data['name']}): {data['qty']} units in stock. Status: {data['status']}"

    return "\n".join([
        f"{sku}: {info['qty']} units ({info['status']})"
        for sku, info in inventory_data.items()
    ])


@tool
def reorder_inventory(product_sku: str, quantity: int, priority: str = "normal") -> str:
    """Generate a reorder recommendation or purchase order.

    Args:
        product_sku: Product SKU to reorder
        quantity: Quantity to order
        priority: Priority level ("normal", "rush", "critical")

    Returns:
        Reorder confirmation with estimated delivery timeline
    """
    lead_times = {
        "normal": "5-7 business days",
        "rush": "2-3 business days",
        "critical": "1 business day (express)",
    }

    delivery = lead_times.get(priority, "5-7 business days")

    return f"""Reorder Created:
- Product: {product_sku}
- Quantity: {quantity} units
- Priority: {priority}
- Estimated Delivery: {delivery}
- PO Status: Generated and sent to supplier"""


@tool
def get_inventory_alerts() -> str:
    """Get all inventory alerts requiring attention.

    Returns:
        List of inventory alerts including low stock, out of stock, and overstock items
    """
    alerts = [
        {"sku": "SKU-004", "type": "critical", "message": "Gadget X below safety stock - immediate reorder needed"},
        {"sku": "SKU-002", "type": "warning", "message": "Widget B approaching reorder point"},
        {"sku": "SKU-005", "type": "critical", "message": "Gadget Y out of stock - backorder initiated"},
    ]

    return "\n".join([
        f"[{alert['type'].upper()}] {alert['sku']}: {alert['message']}"
        for alert in alerts
    ])


@tool
def calculate_eoq(annual_demand: float, ordering_cost: float, holding_cost_rate: float) -> str:
    """Calculate Economic Order Quantity.

    EOQ = sqrt(2 × D × S / H)
    Where:
    - D = Annual demand
    - S = Ordering cost per order
    - H = Holding cost per unit per year (holding_cost_rate × unit_cost)

    Args:
        annual_demand: Expected annual demand in units
        ordering_cost: Cost to place one order
        holding_cost_rate: Annual holding cost as percentage of unit cost

    Returns:
        Optimal order quantity and cost analysis
    """
    import math

    eoq = math.sqrt(2 * annual_demand * ordering_cost / holding_cost_rate)
    total_orders = annual_demand / eoq if eoq > 0 else 0
    total_holding = (eoq / 2) * holding_cost_rate

    return f"""EOQ Analysis:
- Optimal Order Quantity: {eoq:.0f} units
- Number of Orders per Year: {total_orders:.1f}
- Annual Holding Cost: ${total_holding:.2f}
- Recommendation: Order {eoq:.0f} units per order to minimize total inventory costs"""


# Tool list for export
INVENTORY_TOOLS = [check_stock_levels, reorder_inventory, get_inventory_alerts, calculate_eoq]


def create_inventory_agent(model_name: str | None = None, temperature: float | None = None):
    """Create the inventory management agent."""
    model_name = model_name or get_inventory_model()
    temperature = temperature if temperature is not None else get_model_temperature()
    model = ChatOpenAI(model=model_name, temperature=temperature)
    return create_agent(
        model=model,
        tools=INVENTORY_TOOLS,
        system_prompt=INVENTORY_SYSTEM_PROMPT,
    )