"""Runnable entry point for one real card-choice Agent turn."""

import json
from pathlib import Path
from typing import Any

from assistant.card_tools import get_card_facts
from assistant.openai_model import (
    CARD_TOOL_SPEC,
    DECISION_TEXT_FORMAT,
    build_system_instructions,
)
from assistant.runtime import TurnContract, run_decision

FIXTURE_PATH = (
    Path(__file__).parent.parent
    / "tests"
    / "fixtures"
    / "ironclad_card_reward.json"
)


def validate_card_decision(
    observation: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:
    """Return a legal decision or raise ``ValueError``.

    Legal choices are the current ``offered_card_ids`` plus ``skip`` only when
    ``can_skip`` is true. This task-level gate is the human-owned core of
    Phase 1B.
    """
    choice = decision["choice"]
    if choice in observation["offered_card_ids"]:
        return decision
    if choice == "skip" and observation["can_skip"]:
        return decision
    raise ValueError(f"Invalid decision: {decision}")


def validate_tool_request(
    observation: dict[str, Any],
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """Return legal tool arguments or raise ``ValueError``.

    This task-level pre-execution gate is the human-owned core of Phase 1C.
    """
    if tool_name != "get_card_facts":
        raise ValueError(f"Invalid tool name: {tool_name}")
    if arguments["card_id"] not in observation["offered_card_ids"]:
        raise ValueError(f"Invalid card id: {arguments['card_id']}")
    return arguments


def build_card_turn_contract(
    observation: dict[str, Any],
    catalog: dict[str, dict[str, Any]],
) -> TurnContract:
    """Bind card instructions, capabilities, and guards to current state."""

    def guarded_get_card_facts(card_id: str) -> dict[str, Any]:
        arguments = validate_tool_request(
            observation,
            "get_card_facts",
            {"card_id": card_id},
        )
        return get_card_facts(arguments["card_id"], catalog)

    def validate_final(decision: dict[str, Any]) -> dict[str, Any]:
        return validate_card_decision(observation, decision)

    return TurnContract(
        instructions=build_system_instructions(),
        tool_specs=[CARD_TOOL_SPEC],
        text_format=DECISION_TEXT_FORMAT,
        tools={"get_card_facts": guarded_get_card_facts},
        validate_decision=validate_final,
    )


def run_live_decision(
    client: Any,
    fixture_path: Path = FIXTURE_PATH,
) -> dict[str, Any]:
    """Build current card state and delegate to the shared Agent Runtime."""
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    source = fixture["observation"]
    catalog = {
        card["id"]: card
        for card in source["offered_cards"]
    }
    observation = {
        "offered_card_ids": list(catalog),
        "can_skip": source["can_skip"],
        "deck_summary": source["deck_summary"],
    }
    contract = build_card_turn_contract(observation, catalog)
    return run_decision(client, observation, contract)


def main() -> None:
    """Create the real OpenAI client and print one Agent decision."""
    from openai import OpenAI

    result = run_live_decision(OpenAI())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
