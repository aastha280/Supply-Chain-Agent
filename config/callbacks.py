from langchain_core.callbacks import BaseCallbackHandler
from typing import Dict, Any, List, Optional
from uuid import UUID

from rich.console import Console

console = Console()

class RichTerminalCallbackHandler(BaseCallbackHandler):
    """A custom callback handler that logs internal tool steps using Rich."""

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        inputs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when tool starts running."""
        tool_name = serialized.get("name", "tool")
        if tool_name != "task_dispatcher":
            console.print(f"[bold yellow]  -> Running sub-task:[/bold yellow] [italic]{tool_name}[/italic]")

    def on_tool_end(
        self,
        output: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when tool ends running."""
        # By default we keep it clean. We could log the result here as well if needed.
        pass
