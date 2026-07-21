import json
import unittest
from pathlib import Path
from types import SimpleNamespace

from assistant.agent_loop import run_agent_turn
from assistant.card_tools import get_card_facts
from assistant.openai_model import (
    CARD_TOOL_SPEC,
    DECISION_TEXT_FORMAT,
    DEFAULT_MODEL,
    OpenAIResponsesModel,
    build_system_instructions,
)


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "ironclad_card_reward.json"


class FakeResponses:
    def __init__(self) -> None:
        self.requests = []

    def create(self, **request):
        self.requests.append(request)
        if len(self.requests) == 1:
            return SimpleNamespace(
                id="resp-1",
                output=[
                    SimpleNamespace(
                        type="function_call",
                        call_id="call-1",
                        name="get_card_facts",
                        arguments='{"card_id":"shrug_it_off"}',
                    )
                ],
                output_text="",
            )
        return SimpleNamespace(
            id="resp-2",
            output=[SimpleNamespace(type="message")],
            output_text='{"choice":"shrug_it_off","reason":"Adds Block and draw."}',
        )


class OpenAIModelTest(unittest.TestCase):
    def test_real_model_boundary_preserves_the_agent_contract(self) -> None:
        source = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))["observation"]
        catalog = {card["id"]: card for card in source["offered_cards"]}
        observation = {
            "offered_card_ids": list(catalog),
            "can_skip": source["can_skip"],
            "deck_summary": source["deck_summary"],
        }
        context = [{"type": "observation", "content": observation}]
        fake_responses = FakeResponses()
        fake_client = SimpleNamespace(responses=fake_responses)
        model = OpenAIResponsesModel(
            client=fake_client,
            instructions=build_system_instructions(),
            tool_specs=[CARD_TOOL_SPEC],
            text_format=DECISION_TEXT_FORMAT,
        )
        tools = {
            "get_card_facts": lambda card_id: get_card_facts(card_id, catalog)
        }

        result = run_agent_turn(context, model, tools)

        self.assertEqual(DEFAULT_MODEL, fake_responses.requests[0]["model"])
        self.assertNotIn("previous_response_id", fake_responses.requests[0])
        self.assertEqual(
            "resp-1", fake_responses.requests[1]["previous_response_id"]
        )
        self.assertEqual(
            "function_call_output", fake_responses.requests[1]["input"][0]["type"]
        )
        self.assertEqual("call-1", fake_responses.requests[1]["input"][0]["call_id"])
        self.assertEqual(
            ["observation", "tool_call", "tool_result", "final"],
            [event["type"] for event in result["trace"]],
        )
        self.assertIn(result["decision"]["choice"], observation["offered_card_ids"])


if __name__ == "__main__":
    unittest.main()
