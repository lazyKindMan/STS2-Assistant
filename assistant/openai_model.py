"""OpenAI Responses API adapter for the provider-neutral Agent loop."""

import json
from typing import Any, Optional


DEFAULT_MODEL = "gpt-5.6-sol"

CARD_TOOL_SPEC = {
    "type": "function",
    "name": "get_card_facts",
    "description": "Return sourced facts for one offered card ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "card_id": {
                "type": "string",
                "description": "One card ID from observation.offered_card_ids.",
            }
        },
        "required": ["card_id"],
        "additionalProperties": False,
    },
    "strict": True,
}

DECISION_TEXT_FORMAT = {
    "format": {
        "type": "json_schema",
        "name": "card_decision",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "choice": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["choice", "reason"],
            "additionalProperties": False,
        },
    }
}


def build_system_instructions() -> str:
    """Return the card-choice policy supplied to every Responses API turn."""
    return (
        "You are a Slay the Spire 2 card-choice agent. Use only the current "
        "observation and tool results. Before making a final decision, call "
        "get_card_facts exactly once for one ID in offered_card_ids. After the "
        "tool result arrives, choose only an offered card ID, or choose skip "
        "only when can_skip is true. Give a short reason grounded in the "
        "observation and returned card facts. Do not invent card facts."
    )


def normalize_openai_response(response: Any) -> dict[str, Any]:
    """Convert an OpenAI response to the Agent's tool_call/final contract.

    This provider-boundary conversion is the human-owned core of iteration 3A.
    """
    output = getattr(response, "output", None)
    tool_call_output = []
    if output is None:
        raise ValueError("Expected an OpenAI response")
    for resp in output:
        if resp.type != "function_call":
            continue
        tool_call_output.append({
            "type": "tool_call",
            "call_id": resp.call_id,
            "name": resp.name,
            "arguments": json.loads(resp.arguments),
        })
    if len(tool_call_output) > 1:
        raise ValueError("Expected at most one tool call")
    elif len(tool_call_output) == 1:
        return tool_call_output[0]
    else:
        return {"type": "final", "decision": json.loads(response.output_text)}



class OpenAIResponsesModel:
    """Translate OpenAI Responses API items to internal Agent events."""

    def __init__(
        self,
        client: Any,
        instructions: str,
        model: str = DEFAULT_MODEL,
    ) -> None:
        self.client = client
        self.instructions = instructions
        self.model = model
        self.previous_response_id: Optional[str] = None

    def __call__(self, context: list[dict[str, Any]]) -> dict[str, Any]:
        request: dict[str, Any] = {
            "model": self.model,
            "instructions": self.instructions,
            "tools": [CARD_TOOL_SPEC],
            "text": DECISION_TEXT_FORMAT,
            "reasoning": {"effort": "low"},
        }

        if self.previous_response_id is None:
            request["input"] = [
                {
                    "role": "user",
                    "content": json.dumps(context, ensure_ascii=False),
                }
            ]
        else:
            tool_result = context[-1]
            if tool_result.get("type") != "tool_result":
                raise ValueError("Expected the latest context event to be tool_result")
            request["previous_response_id"] = self.previous_response_id
            request["input"] = [
                {
                    "type": "function_call_output",
                    "call_id": tool_result["call_id"],
                    "output": json.dumps(tool_result["content"], ensure_ascii=False),
                }
            ]

        response = self.client.responses.create(**request)
        self.previous_response_id = response.id

        return normalize_openai_response(response)
