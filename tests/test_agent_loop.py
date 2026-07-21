import json
import unittest
from copy import deepcopy
from pathlib import Path

from assistant.agent_loop import run_agent_turn
from assistant.card_tools import get_card_facts


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "ironclad_card_reward.json"


class AgentLoopTest(unittest.TestCase):
    def test_rejects_an_unknown_tool_before_any_handler_runs(self) -> None:
        handler_calls = []

        def scripted_model(_context):
            return {
                "type": "tool_call",
                "call_id": "call-unknown",
                "name": "unknown_tool",
                "arguments": {},
            }

        def registered_handler():
            handler_calls.append("called")
            return {}

        with self.assertRaisesRegex(ValueError, "Unknown tool"):
            run_agent_turn(
                [],
                scripted_model,
                {"get_card_facts": registered_handler},
            )

        self.assertEqual([], handler_calls)

    def test_feeds_one_tool_result_into_the_next_model_turn(self) -> None:
        source = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))["observation"]
        catalog = {card["id"]: card for card in source["offered_cards"]}
        observation = {
            "character": source["character"],
            "current_hp": source["current_hp"],
            "max_hp": source["max_hp"],
            "deck_summary": source["deck_summary"],
            "offered_card_ids": list(catalog),
            "can_skip": source["can_skip"],
        }
        initial_context = [
            {
                "type": "instructions",
                "content": {
                    "goal": "Choose one legal card or skip.",
                    "allowed_tools": ["get_card_facts"],
                },
            },
            {"type": "observation", "content": observation},
        ]
        scripted_responses = [
            {
                "type": "tool_call",
                "call_id": "call-1",
                "name": "get_card_facts",
                "arguments": {"card_id": "shrug_it_off"},
            },
            {
                "type": "final",
                "decision": {
                    "choice": "shrug_it_off",
                    "reason": "Adds Block and card draw.",
                },
            },
        ]
        contexts_seen = []

        def scripted_model(context):
            contexts_seen.append(deepcopy(context))
            return scripted_responses[len(contexts_seen) - 1]

        tools = {
            "get_card_facts": lambda card_id: get_card_facts(card_id, catalog)
        }

        result = run_agent_turn(initial_context, scripted_model, tools)

        self.assertEqual(2, len(contexts_seen))
        self.assertEqual("tool_result", contexts_seen[1][-1]["type"])
        self.assertEqual("call-1", contexts_seen[1][-1]["call_id"])
        self.assertEqual("shrug_it_off", contexts_seen[1][-1]["content"]["id"])
        self.assertEqual(
            ["instructions", "observation", "tool_call", "tool_result", "final"],
            [event["type"] for event in result["trace"]],
        )
        self.assertEqual("shrug_it_off", result["decision"]["choice"])
        self.assertIn(result["decision"]["choice"], observation["offered_card_ids"])


if __name__ == "__main__":
    unittest.main()
