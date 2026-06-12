"""Supply chain utility tools for cross-agent functionality."""

from langchain.tools import tool


@tool
def get_inventory_summary() -> str:
    """Get a high-level summary of inventory status across all products.

    Returns:
        Summary of inventory health including stock levels, alerts, and recommendations
    """
    return """Inventory Summary:

Stock Status:
- Adequate Stock: 2 products (SKU-001, SKU-003)
- Low Stock: 1 product (SKU-002)
- Critical Stock: 1 product (SKU-004)
- Out of Stock: 1 product (SKU-005)

Actions Required:
- Immediate reorder: SKU-004 (Gadget X)
- Review reorder: SKU-002 (Widget B)

Overall Inventory Health: Needs Attention
Fill Rate: 87%
Average Days of Supply: 18 days"""


@tool
def get_supply_chain_kpi() -> str:
    """Get key performance indicators for the supply chain.

    Returns:
        KPI dashboard with current metrics
    """
    return """Supply Chain KPIs:

EFFICIENCY
- Inventory Turnover: 6.2x/year
- Order Accuracy: 98.5%
- On-Time In-Full (OTIF): 94.2%

COST
- Carrying Cost: $45,000/month
- Ordering Cost: $12,000/month
- Total Inventory Value: $1.2M

SUPPLIER
- Supplier Lead Time (Avg): 7 days
- Supplier Quality Score: 4.4/5.0
- Single Source Dependency: 15%

RISK
- Risk Score: 6.5/10 (Medium-High)
- Active Disruptions: 1
- Recovery Time Objective: 14 days"""


@tool
def generate_reorder_recommendation(product_sku: str) -> str:
    """Generate a comprehensive reorder recommendation for a product.

    Args:
        product_sku: Product SKU to generate recommendation for

    Returns:
        Full recommendation with quantities, supplier suggestions, and timing
    """
    return f"""Reorder Recommendation for {product_sku}:

Current Status:
- Stock Level: LOW/CRITICAL
- Days of Supply: < 7 days

Recommendation:
1. Order Quantity: 200 units
2. Suggested Supplier: SUP-002 (fastest delivery)
3. Priority: RUSH
4. Expected Delivery: 2-3 business days
5. Estimated Cost: $3,150

Long-term Actions:
- Review safety stock levels for this product
- Qualify secondary supplier to reduce lead time risk
- Consider setting up automatic reorder triggers"""


@tool
def analyze_supply_chain_performance(time_period: str = "30d") -> str:
    """Analyze overall supply chain performance over a time period.

    Args:
        time_period: Analysis period ("7d", "30d", "90d", "1y")

    Returns:
        Performance analysis with trends and recommendations
    """
    return f"""Supply Chain Performance Analysis ({time_period}):

STRENGTHS:
- Order fulfillment rate improved 3%
- Supplier quality scores stable
- Logistics costs under budget

WEAKNESSES:
- Inventory days increased by 2 days
- Two suppliers below target OTIF
- Risk alerts increased 15%

OPPORTUNITIES:
- Implement VMI with top supplier
- Consolidate shipments to reduce logistics costs
- Expand dual-sourcing for critical components

THREATS:
- Geopolitical risk elevated for APAC suppliers
- Q4 capacity constraints expected
- Raw material inflation pressure

Overall Assessment: Stable but needs proactive risk management"""