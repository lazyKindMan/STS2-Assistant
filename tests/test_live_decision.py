import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from assistant.live_decision import (
    run_live_decision,
    validate_card_decision,
    validate_tool_request,
)


class FakeResponses:
    def __init__(self, card_id="shrug_it_off") -> None:
        self.requests = []
        self.card_id = card_id

    def create(self, **request):
        self.requests.append(request)
        request_number = len(self.requests)
        if request_number % 2 == 1:
            return SimpleNamespace(
                id=f"resp-live-{request_number}",
                output=[
                    SimpleNamespace(
                        type="function_call",
                        call_id=f"call-live-{request_number}",
                        name="get_card_facts",
                        arguments=json.dumps({"card_id": self.card_id}),
                    )
                ],
                output_text="",
            )
        return SimpleNamespace(
            id=f"resp-live-{request_number}",
            output=[SimpleNamespace(type="message")],
            output_text=json.dumps(
                {
                    "choice": "shrug_it_off",
                    "reason": "Adds Block and card draw.",
                }
            ),
        )


class LiveDecisionTest(unittest.TestCase):
    def test_rejects_a_tool_name_outside_the_task_allowlist(self) -> None:
        observation = {
            "offered_card_ids": ["card_a"],
            "can_skip": False,
        }

        with self.assertRaises(ValueError):
            validate_tool_request(
                observation,
                "unknown_tool",
                {"card_id": "card_a"},
            )

    def test_rejects_an_unoffered_tool_argument_before_execution(self) -> None:
        responses = FakeResponses(card_id="card_x")
        client = SimpleNamespace(responses=responses)

        with patch("assistant.live_decision.get_card_facts") as handler:
            with self.assertRaises(ValueError):
                run_live_decision(client)

        handler.assert_not_called()

    def test_rejects_choices_outside_the_current_legal_actions(self) -> None:
        observation = {
            "offered_card_ids": ["card_a", "card_b", "card_c"],
            "can_skip": False,
        }

        with self.assertRaises(ValueError):
            validate_card_decision(
                observation,
                {"choice": "card_x", "reason": "Invented choice."},
            )
        with self.assertRaises(ValueError):
            validate_card_decision(
                observation,
                {"choice": "skip", "reason": "Skip is disabled."},
            )

        valid = {"choice": "card_a", "reason": "It is offered."}
        self.assertEqual(valid, validate_card_decision(observation, valid))

    def test_composes_one_complete_model_tool_turn(self) -> None:
        responses = FakeResponses()
        client = SimpleNamespace(responses=responses)

        result = run_live_decision(client)

        self.assertEqual(2, len(responses.requests))
        self.assertEqual(
            ["observation", "tool_call", "tool_result", "final"],
            [event["type"] for event in result["trace"]],
        )
        self.assertEqual("shrug_it_off", result["decision"]["choice"])

    def test_two_independent_turns_start_with_fresh_provider_context(self) -> None:
        responses = FakeResponses()
        client = SimpleNamespace(responses=responses)

        run_live_decision(client)
        run_live_decision(client)
        self.assertEqual(4, len(responses.requests))
        # Human-owned core: assert the four requests prove both of these rules:
        # 1. each turn's second request continues from that turn's first response;
        self.assertNotIn("previous_response_id", responses.requests[0].keys())
        self.assertEqual(responses.requests[1]["previous_response_id"], "resp-live-1")
        # 2. the second turn's first request does not continue from the first turn.
        self.assertNotIn("previous_response_id", responses.requests[2].keys())
        self.assertEqual(responses.requests[3]["previous_response_id"], "resp-live-3")



if __name__ == "__main__":
    unittest.main()
