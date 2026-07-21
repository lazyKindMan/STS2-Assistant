"""Local read-only tools used by the Agent-loop lessons."""

from typing import Any


def get_card_facts(
    card_id: str, card_catalog: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """Return a copy of one card's sourced facts from the local catalog."""
    if card_id not in card_catalog:
        raise ValueError(f"Unknown card id: {card_id}")
    return dict(card_catalog[card_id])
