"""Demand Forecasting Agent - Analyzes demand patterns and predicts future demand."""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from config.settings import get_demand_model, get_model_temperature


DEMAND_SYSTEM_PROMPT = """You are a Demand Forecasting Analyst specializing in predicting future
product demand using statistical analysis and machine learning techniques.

Your expertise includes:
- Time series analysis (trend, seasonality, cyclical patterns)
- Moving averages and exponential smoothing methods
- Demand variability analysis (standard deviation, coefficient of variation)
- Seasonal indices calculation and application
- External factor correlation (weather, promotions, economic indicators)

You help users understand past demand patterns and make informed forecasts
for inventory planning and production scheduling."""


@tool
def forecast_demand(product_sku: str, periods: int = 12, method: str = "auto") -> str:
    """Generate a demand forecast for a product.

    Args:
        product_sku: Product SKU to forecast
        periods: Number of future periods to forecast (default: 12)
        method: Forecasting method ("auto", "simple", "seasonal", "trend")

    Returns:
        Demand forecast with confidence intervals
    """
    import random

    # Simulated forecast data - in production, use actual statistical models
    base_demand = random.randint(80, 200)

    if method == "simple":
        forecast = [base_demand] * periods
        method_desc = "Simple moving average"
    elif method == "seasonal":
        # Add seasonal variation
        forecast = [base_demand * (1 + 0.3 * ((i % 12) / 6 - 1) ** 2) for i in range(periods)]
        method_desc = "Seasonal adjustment applied"
    elif method == "trend":
        # Add upward trend
        forecast = [base_demand * (1 + 0.02 * i) for i in range(periods)]
        method_desc = "Linear trend projection"
    else:
        # Auto selects best method
        forecast = [base_demand * (1 + 0.1 * (i % 3 - 1)) for i in range(periods)]
        method_desc = "Auto-selected (seasonal with trend)"

    confidence_interval = 0.15  # ±15%

    result = f"""Demand Forecast for {product_sku} ({method_desc}):

Period | Forecast | Low (85%) | High (85%)
-------|----------|-----------|------------"""

    for i, units in enumerate(forecast, 1):
        low = units * (1 - confidence_interval)
        high = units * (1 + confidence_interval)
        result += f"\n  {i:2d}   |   {units:5.0f}   |   {low:5.0f}    |   {high:5.0f}"

    result += f"""

Summary Statistics:
- Average Forecast: {sum(forecast)/len(forecast):.0f} units/period
- Min Forecast: {min(forecast):.0f} units
- Max Forecast: {max(forecast):.0f} units
- Total {periods}-Period Demand: {sum(forecast):.0f} units"""

    return result


@tool
def analyze_seasonality(product_sku: str | None = None) -> str:
    """Analyze seasonal patterns in demand data.

    Args:
        product_sku: Product SKU to analyze (None for all products)

    Returns:
        Seasonal indices and pattern analysis
    """
    import random

    # Simulated seasonal indices
    products = {
        "SKU-001": {"name": "Widget A", "seasonal_pattern": "Q4 peak (holiday)", "indices": [0.7, 0.8, 0.9, 1.6]},
        "SKU-002": {"name": "Widget B", "seasonal_pattern": "Q1/Q2 peak (spring)", "indices": [1.2, 1.3, 0.9, 0.6]},
        "SKU-003": {"name": "Widget C", "seasonal_pattern": "Steady (no seasonality)", "indices": [1.0, 1.0, 1.0, 1.0]},
    }

    if product_sku and product_sku in products:
        data = products[product_sku]
        indices_str = " | ".join([f"Q{i+1}: {idx:.2f}" for i, idx in enumerate(data["indices"])])
        return f"{product_sku} ({data['name']}): {data['seasonal_pattern']}\nSeasonal Indices: {indices_str}"

    result = "Seasonal Pattern Analysis:\n\n"
    for sku, data in products.items():
        indices_str = " | ".join([f"Q{i+1}: {idx:.2f}" for i, idx in enumerate(data["indices"])])
        result += f"{sku} ({data['name']}): {data['seasonal_pattern']}\n  Indices: {indices_str}\n\n"

    return result


@tool
def get_demand_trends(product_sku: str | None = None, period: str = "90d") -> str:
    """Get recent demand trends for products.

    Args:
        product_sku: Product SKU (None for all products)
        period: Time period ("30d", "90d", "1y")

    Returns:
        Demand trend analysis including growth rates and volatility
    """
    trends = {
        "SKU-001": {"trend": "upward", "growth_rate": "+12%", "volatility": "low"},
        "SKU-002": {"trend": "stable", "growth_rate": "+2%", "volatility": "medium"},
        "SKU-003": {"trend": "downward", "growth_rate": "-8%", "volatility": "high"},
        "SKU-004": {"trend": "upward", "growth_rate": "+25%", "volatility": "medium"},
    }

    if product_sku:
        if product_sku in trends:
            data = trends[product_sku]
            return f"{product_sku}: Trend={data['trend']}, Growth={data['growth_rate']}, Volatility={data['volatility']}"
        return f"{product_sku}: No data available"

    result = "Demand Trends (Last " + period + "):\n\n"
    result += "SKU      | Trend    | Growth | Volatility\n"
    result += "---------|----------|--------|------------\n"
    for sku, data in trends.items():
        result += f"{sku:8} | {data['trend']:8} | {data['growth_rate']:6} | {data['volatility']}\n"

    return result


DEMAND_TOOLS = [forecast_demand, analyze_seasonality, get_demand_trends]


def create_demand_agent(model_name: str | None = None, temperature: float | None = None):
    """Create the demand forecasting agent."""
    model_name = model_name or get_demand_model()
    temperature = temperature if temperature is not None else get_model_temperature()
    model = ChatOpenAI(model=model_name, temperature=temperature)
    return create_agent(
        model=model,
        tools=DEMAND_TOOLS,
        system_prompt=DEMAND_SYSTEM_PROMPT,
    )