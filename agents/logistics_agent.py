"""Logistics Coordinator Agent - Handles shipping, route optimization, and delivery tracking."""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from config.settings import get_logistics_model, get_model_temperature


LOGISTICS_SYSTEM_PROMPT = """You are a Logistics Coordinator specializing in shipping operations,
route optimization, and delivery management.

Your expertise includes:
- Shipment scheduling and carrier selection
- Route optimization algorithms (traveling salesman, vehicle routing)
- Delivery time estimation and tracking
- Freight cost optimization
- Multi-modal transportation planning (air, sea, truck, rail)
- Last-mile delivery challenges

You help users manage the physical movement of goods through the supply chain."""


@tool
def schedule_shipment(
    origin: str,
    destination: str,
    product_sku: str,
    quantity: int,
    carrier: str | None = None,
    shipping_method: str = "standard",
) -> str:
    """Schedule a new shipment.

    Args:
        origin: Origin location/warehouse code
        destination: Destination address or code
        product_sku: Product being shipped
        quantity: Number of units
        carrier: Preferred carrier (None for best price)
        shipping_method: "standard", "express", or "economy"

    Returns:
        Shipment details with cost estimate and delivery date
    """
    carriers = {
        "standard": ["FedEx Ground", "UPS Ground", "USPS"],
        "express": ["FedEx Express", "UPS Next Day", "DHL Express"],
        "economy": ["Old Dominion", "SAIA", "XPO"],
    }

    methods = {
        "standard": {"transit": "5-7 days", "cost_per_unit": 2.50},
        "express": {"transit": "1-2 days", "cost_per_unit": 8.00},
        "economy": {"transit": "7-10 days", "cost_per_unit": 1.50},
    }

    selected_carrier = carrier or carriers[shipping_method][0]
    method_info = methods[shipping_method]
    total_cost = method_info["cost_per_unit"] * quantity

    import random
    ship_id = f"SHIP-{random.randint(100000, 999999)}"

    return f"""Shipment Scheduled:
- Shipment ID: {ship_id}
- From: {origin}
- To: {destination}
- Carrier: {selected_carrier}
- Method: {shipping_method.title()}
- Transit Time: {method_info['transit']}
- Product: {product_sku} × {quantity}
- Estimated Cost: ${total_cost:.2f}
- Status: Pickup scheduled"""


@tool
def track_delivery(shipment_id: str) -> str:
    """Track a shipment by ID.

    Args:
        shipment_id: Shipment tracking ID

    Returns:
        Current status, location, and ETA
    """
    import random

    statuses = [
        {"status": "In Transit", "location": "Memphis, TN Hub", "progress": 45, "eta": "2 days"},
        {"status": "Out for Delivery", "location": "Local Delivery Station", "progress": 90, "eta": "Today by 5PM"},
        {"status": "Delivered", "location": "Destination", "progress": 100, "eta": "Delivered"},
        {"status": "Processing", "location": "Origin Warehouse", "progress": 10, "eta": "4 days"},
    ]

    # Simulated tracking - in production, call carrier API
    data = statuses[random.randint(0, len(statuses) - 1)]

    return f"""Tracking: {shipment_id}

Status: {data['status']}
Location: {data['location']}
Progress: {'█' * int(data['progress']/10)}{'░' * (10 - int(data['progress']/10))} {data['progress']}%
ETA: {data['eta']}"""


@tool
def optimize_routes(
    origin: str,
    destinations: list[str],
    vehicle_capacity: int = 100,
) -> str:
    """Optimize delivery routes for multiple stops.

    Args:
        origin: Starting location/warehouse
        destinations: List of destination addresses
        vehicle_capacity: Maximum units per vehicle

    Returns:
        Optimized route sequence with estimated times and costs
    """
    # Simplified route optimization - in production, use OR tools or APIs
    num_stops = len(destinations)
    base_miles = 50  # Base miles per stop

    route = f"""Route Optimization Results:

Starting Point: {origin}
Stops: {num_stops}
Vehicle Capacity: {vehicle_capacity} units

Optimized Route Sequence:
"""

    for i, dest in enumerate(destinations, 1):
        route += f"  {i}. {dest}\n"

    route += f"""
Estimated Metrics:
- Total Distance: {num_stops * base_miles} miles
- Estimated Drive Time: {num_stops * 25} minutes
- Fuel Cost: ${num_stops * 3.50:.2f}
- CO2 Emissions: {num_stops * 12:.1f} lbs

Recommendations:
- Split into {(num_stops + vehicle_capacity - 1) // vehicle_capacity} batches for capacity optimization
- Consider morning deliveries for time-sensitive products"""

    return route


@tool
def get_shipping_rates(origin: str, destination: str, weight: float) -> str:
    """Get shipping rate quotes from multiple carriers.

    Args:
        origin: Origin zip code
        destination: Destination zip code
        weight: Package weight in lbs

    Returns:
        Rate comparison from various carriers
    """
    carriers = [
        {"name": "FedEx", "ground": 12.50, "express": 45.00, "economy": 8.50},
        {"name": "UPS", "ground": 11.75, "express": 42.50, "economy": 9.25},
        {"name": "USPS", "ground": 9.50, "express": 35.00, "economy": 6.50},
        {"name": "DHL", "ground": 14.00, "express": 55.00, "economy": 10.00},
    ]

    result = f"Shipping Rates: {origin} → {destination} ({weight} lbs)\n\n"
    result += "Carrier | Ground  | Express | Economy\n"
    result += "--------|---------|---------|--------\n"

    for c in carriers:
        result += f"{c['name']:7} | ${c['ground']:6.2f} | ${c['express']:6.2f} | ${c['economy']:6.2f}\n"

    result += "\nBest Value: USPS Economy (Ground)"
    result += "\nFastest: FedEx/UPS Express"

    return result


LOGISTICS_TOOLS = [schedule_shipment, track_delivery, optimize_routes, get_shipping_rates]


def create_logistics_agent(model_name: str | None = None, temperature: float | None = None):
    """Create the logistics coordinator agent."""
    model_name = model_name or get_logistics_model()
    temperature = temperature if temperature is not None else get_model_temperature()
    model = ChatOpenAI(model=model_name, temperature=temperature)
    return create_agent(
        model=model,
        tools=LOGISTICS_TOOLS,
        system_prompt=LOGISTICS_SYSTEM_PROMPT,
    )