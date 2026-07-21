"""Build the bounded observation for one route-choice turn."""

from typing import Any


def build_route_observation(game_state: dict[str, Any]) -> dict[str, Any]:
    """Expose useful map topology and the nodes reachable on this step.

    ``game_state`` is a fresh manual snapshot. The current node's
    ``outgoing_node_ids`` define the legal route actions for this turn.

    This state-to-observation conversion is the human-owned core of Phase 2A.
    """
    current_node_id = game_state["current_node_id"]
    reachable_node_ids = []
    for node in game_state["nodes"]:
        if node["id"] == current_node_id:
            reachable_node_ids = node["outgoing_node_ids"]
    return {
        "character": game_state["character"],
        "current_hp": game_state["current_hp"],
        "max_hp": game_state["max_hp"],
        "act": game_state["act"],
        "current_node_id": current_node_id,
        "nodes": game_state["nodes"],
        "reachable_node_ids": reachable_node_ids,
    }