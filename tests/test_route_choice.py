import json
import unittest
from pathlib import Path

from assistant.route_choice import build_route_observation


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "ironclad_route_choice.json"


class BuildRouteObservationTest(unittest.TestCase):
    def test_exposes_full_topology_and_only_current_reachable_nodes(self) -> None:
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        game_state = fixture["game_state"]

        observation = build_route_observation(game_state)

        self.assertEqual("ironclad", observation["character"])
        self.assertEqual(52, observation["current_hp"])
        self.assertEqual(80, observation["max_hp"])
        self.assertEqual(1, observation["act"])
        self.assertEqual("start", observation["current_node_id"])
        self.assertEqual(["elite_1", "shop_1"], observation["reachable_node_ids"])

        visible_node_ids = {node["id"] for node in observation["nodes"]}
        self.assertEqual(
            {"start", "elite_1", "shop_1", "rest_2"},
            visible_node_ids,
        )
        self.assertNotIn("rest_2", observation["reachable_node_ids"])


if __name__ == "__main__":
    unittest.main()
