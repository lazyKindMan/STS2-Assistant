"""Compose one fake or real OpenAI-backed route-decision Agent turn."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from assistant.route_choice import build_route_observation
from assistant.route_tools import inspect_route_path
from assistant.runtime import TurnContract, run_decision


FIXTURE_PATH = (
    Path(__file__).parent.parent
    / "tests"
    / "fixtures"
    / "ironclad_route_choice.json"
)

ROUTE_TOOL_SPEC = {
    "type": "function",
    "name": "inspect_route_path",
    "description": "Inspect one currently reachable node and its next nodes.",
    "parameters": {
        "type": "object",
        "properties": {
            "node_id": {
                "type": "string",
                "description": "One node ID from observation.reachable_node_ids.",
            }
        },
        "required": ["node_id"],
        "additionalProperties": False,
    },
    "strict": True,
}

ROUTE_DECISION_TEXT_FORMAT = {
    "format": {
        "type": "json_schema",
        "name": "route_decision",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "choice": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["choice", "reason"],
            "additionalProperties": False,
        },
    }
}


def build_route_system_instructions() -> str:
    """Return the task instructions for one route-choice turn."""
    return (
        "You are a Slay the Spire 2 route-choice agent. Use only the current "
        "observation and tool results. Before making a final decision, call "
        "inspect_route_path exactly once for one ID in reachable_node_ids. "
        "After the tool result arrives, choose only an ID in "
        "reachable_node_ids and give a short reason. Do not invent nodes or "
        "execute movement."
    )


def validate_route_tool_request(
    observation: dict[str, Any],
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """Reject an unavailable route tool or unreachable node before execution."""
    if tool_name != "inspect_route_path":
        raise ValueError(f"Invalid route tool name: {tool_name}")
    node_id = arguments.get("node_id")
    if node_id not in observation["reachable_node_ids"]:
        raise ValueError(f"Unreachable route tool node: {node_id}")
    return arguments


def validate_route_decision(
    observation: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:
    """Return a reachable route decision or raise ``ValueError``."""
    if decision.get("choice") not in observation["reachable_node_ids"]:
        raise ValueError(f"Unreachable route decision: {decision}")
    return decision


def build_guarded_route_tools(
    observation: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
) -> dict[str, Callable[..., dict[str, Any]]]:
    """Bind current route state to the executable tool boundary."""

    def guarded_inspect_route_path(node_id: str) -> dict[str, Any]:
        arguments = validate_route_tool_request(
            observation,
            "inspect_route_path",
            {"node_id": node_id},
        )
        return inspect_route_path(arguments["node_id"], nodes_by_id)

    return {"inspect_route_path": guarded_inspect_route_path}


def build_route_decision_validator(
    observation: dict[str, Any],
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """Bind the current legal-action set to the final-decision validator."""

    def validator(decision: dict[str, Any]) -> dict[str, Any]:
        return validate_route_decision(observation, decision)

    return validator


def build_route_turn_contract(
    observation: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
) -> TurnContract:
    """Assemble the concrete model, tool, and final-decision route contract.

    Return exactly ``instructions``, ``tool_specs``, ``text_format``, ``tools``,
    and ``validate_decision``. This architecture-level composition is the
    human-owned core of Accelerated Module 1.
    """
    return TurnContract(
        instructions=build_route_system_instructions(),
        tool_specs=[ROUTE_TOOL_SPEC],
        text_format=ROUTE_DECISION_TEXT_FORMAT,
        tools=build_guarded_route_tools(observation, nodes_by_id),
        validate_decision=build_route_decision_validator(observation),
    )


def run_live_route_decision(
    client: Any,
    fixture_path: Path = FIXTURE_PATH,
) -> dict[str, Any]:
    """Run one route Agent turn with an injected fake or real OpenAI client."""
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    observation = build_route_observation(fixture["game_state"])
    nodes_by_id = {node["id"]: node for node in observation["nodes"]}
    contract = build_route_turn_contract(observation, nodes_by_id)
    return run_decision(client, observation, contract)


def main() -> None:
    """Create the real OpenAI client and print one route decision."""
    from openai import OpenAI

    result = run_live_route_decision(OpenAI())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
