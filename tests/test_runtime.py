import json
import unittest
from types import SimpleNamespace

from assistant.runtime import TurnContract, run_decision


class GenericFakeResponses:
    def __init__(self) -> None:
        self.requests = []

    def create(self, **request):
        self.requests.append(request)
        if len(self.requests) == 1:
            return SimpleNamespace(
                id="generic-response-1",
                output=[
                    SimpleNamespace(
                        type="function_call",
                        call_id="generic-call-1",
                        name="inspect_option",
                        arguments=json.dumps({"option_id": "option_a"}),
                    )
                ],
                output_text="",
            )
        return SimpleNamespace(
            id="generic-response-2",
            output=[SimpleNamespace(type="message")],
            output_text=json.dumps(
                {"choice": "option_a", "reason": "The inspected option is legal."}
            ),
        )


class RuntimeTest(unittest.TestCase):
    def test_runs_one_injected_contract_without_knowing_the_task_type(self) -> None:
        responses = GenericFakeResponses()
        client = SimpleNamespace(responses=responses)
        observation = {"legal_action_ids": ["option_a"]}

        def validate_decision(decision):
            if decision["choice"] not in observation["legal_action_ids"]:
                raise ValueError("Illegal generic decision")
            return {
                "choice": decision["choice"],
                "reason": "Normalized by the injected final validator.",
            }

        contract = TurnContract(
            instructions="Inspect and choose one legal generic option.",
            tool_specs=[
                {
                    "type": "function",
                    "name": "inspect_option",
                    "parameters": {
                        "type": "object",
                        "properties": {"option_id": {"type": "string"}},
                        "required": ["option_id"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                }
            ],
            text_format={"format": {"name": "generic_decision"}},
            tools={
                "inspect_option": lambda option_id: {
                    "id": option_id,
                    "status": "legal",
                }
            },
            validate_decision=validate_decision,
        )

        result = run_decision(client, observation, contract)

        self.assertEqual(2, len(responses.requests))
        self.assertEqual(
            ["observation", "tool_call", "tool_result", "final"],
            [event["type"] for event in result["trace"]],
        )
        self.assertEqual("option_a", result["decision"]["choice"])
        self.assertEqual(
            "Normalized by the injected final validator.",
            result["decision"]["reason"],
        )
        self.assertEqual(
            "inspect_option",
            responses.requests[0]["tools"][0]["name"],
        )


if __name__ == "__main__":
    unittest.main()
