"""Small read-only tools for one route-decision turn."""

from typing import Any


def inspect_route_path(
    node_id: str,
    nodes_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Return one candidate node and its immediate downstream nodes."""
    node = nodes_by_id[node_id]
    next_nodes = [
        {
            "id": next_id,
            "type": nodes_by_id[next_id]["type"],
            "floor": nodes_by_id[next_id]["floor"],
        }
        for next_id in node["outgoing_node_ids"]
    ]
    return {
        "node": {
            "id": node["id"],
            "type": node["type"],
            "floor": node["floor"],
        },
        "next_nodes": next_nodes,
    }
