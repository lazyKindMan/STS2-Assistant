import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from assistant.live_route_decision import run_live_route_decision


class FakeRouteResponses:
    def __init__(
        self,
        tool_node_id: str = "elite_1",
        final_choice: str = "elite_1",
    ) -> None:
        self.requests = []
        self.tool_node_id = tool_node_id
        self.final_choice = final_choice

    def create(self, **request):
        self.requests.append(request)
        if len(self.requests) == 1:
            return SimpleNamespace(
                id="route-response-1",
                output=[
                    SimpleNamespace(
                        type="function_call",
                        call_id="route-call-1",
                        name="inspect_route_path",
                        arguments=json.dumps({"node_id": self.tool_node_id}),
                    )
                ],
                output_text="",
            )
        return SimpleNamespace(
            id="route-response-2",
            output=[SimpleNamespace(type="message")],
            output_text=json.dumps(
                {
                    "choice": self.final_choice,
                    "reason": "The inspected path reaches a rest node.",
                }
            ),
        )


class LiveRouteDecisionTest(unittest.TestCase):
    def test_runs_one_complete_route_tool_turn(self) -> None:
        responses = FakeRouteResponses()
        client = SimpleNamespace(responses=responses)

        result = run_live_route_decision(client)

        self.assertEqual(2, len(responses.requests))
        self.assertEqual(
            ["inspect_route_path"],
            [tool["name"] for tool in responses.requests[0]["tools"]],
        )
        self.assertEqual(
            "route_decision",
            responses.requests[0]["text"]["format"]["name"],
        )
        self.assertEqual(
            ["observation", "tool_call", "tool_result", "final"],
            [event["type"] for event in result["trace"]],
        )
        self.assertEqual("elite_1", result["decision"]["choice"])
        self.assertEqual(
            ["rest_2"],
            [node["id"] for node in result["trace"][2]["content"]["next_nodes"]],
        )

    def test_rejects_an_unreachable_tool_node_before_execution(self) -> None:
        responses = FakeRouteResponses(tool_node_id="rest_2")
        client = SimpleNamespace(responses=responses)

        with patch("assistant.live_route_decision.inspect_route_path") as handler:
            with self.assertRaisesRegex(ValueError, "Unreachable route tool node"):
                run_live_route_decision(client)

        handler.assert_not_called()

    def test_rejects_an_unreachable_final_choice(self) -> None:
        responses = FakeRouteResponses(final_choice="rest_2")
        client = SimpleNamespace(responses=responses)

        with self.assertRaisesRegex(ValueError, "Unreachable route decision"):
            run_live_route_decision(client)


if __name__ == "__main__":
    unittest.main()
