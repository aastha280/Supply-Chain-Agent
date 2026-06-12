"""Central configuration for Supply Chain Multi-Agent System.

All settings are loaded from environment variables.
Change values in .env file - no code changes needed.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =============================================================================
# Model Configuration
# =============================================================================

def get_model_name() -> str:
    """Get the LLM model name from environment, with fallback default."""
    return os.getenv("OPENAI_MODEL", "gpt-4.1")


def get_model_temperature() -> float:
    """Get the model temperature from environment, with fallback default."""
    return float(os.getenv("OPENAI_TEMPERATURE", "0"))


# =============================================================================
# Agent-Specific Model Overrides (optional)
# =============================================================================

def get_inventory_model() -> str:
    """Model for inventory agent (uses default if not set)."""
    return os.getenv("MODEL_INVENTORY", get_model_name())

def get_demand_model() -> str:
    """Model for demand agent (uses default if not set)."""
    return os.getenv("MODEL_DEMAND", get_model_name())

def get_logistics_model() -> str:
    """Model for logistics agent (uses default if not set)."""
    return os.getenv("MODEL_LOGISTICS", get_model_name())

def get_supplier_model() -> str:
    """Model for supplier agent (uses default if not set)."""
    return os.getenv("MODEL_SUPPLIER", get_model_name())

def get_risk_model() -> str:
    """Model for risk agent (uses default if not set)."""
    return os.getenv("MODEL_RISK", get_model_name())

def get_orchestrator_model() -> str:
    """Model for orchestrator agent (uses default if not set)."""
    return os.getenv("MODEL_ORCHESTRATOR", get_model_name())