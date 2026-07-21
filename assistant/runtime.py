"""Task-agnostic assembly for one complete Agent decision."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from assistant.agent_loop import ToolCall, run_agent_turn
from assistant.openai_model import OpenAIResponsesModel


DecisionValidator = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class TurnContract:
    """All task-owned capabilities required by the shared Agent Runtime."""

    instructions: str
    tool_specs: list[dict[str, Any]]
    text_format: dict[str, Any]
    tools: dict[str, ToolCall]
    validate_decision: DecisionValidator


def run_decision(
    client: Any,
    observation: dict[str, Any],
    contract: TurnContract,
) -> dict[str, Any]:
    """Run one task-agnostic model/tool/final-decision lifecycle.

    The Runtime must not branch on card or route. It creates the provider
    adapter from ``contract``, runs the existing Agent loop, applies the bound
    final validator, and returns ``decision + trace``.

    This runtime-assembly transition is the human-owned core of Accelerated
    Module 2.
    """
    model = OpenAIResponsesModel(
        client=client,
        instructions=contract.instructions,
        tool_specs=contract.tool_specs,
        text_format=contract.text_format,
    )
    context = [
        {
            "type": "observation",
            "content": observation
        }
    ]
    result = run_agent_turn(context, model, contract.tools)
    result["decision"] = contract.validate_decision(result["decision"])
    return result
