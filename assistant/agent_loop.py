"""One-turn tool-using Agent scaffold."""

from collections.abc import Callable
from typing import Any


ModelCall = Callable[[list[dict[str, Any]]], dict[str, Any]]
ToolCall = Callable[..., dict[str, Any]]

MAX_LOOP_TURNS = 10

def run_agent_turn(
    initial_context: list[dict[str, Any]],
    model: ModelCall,
    tools: dict[str, ToolCall],
    max_model_turns: int = 2,
) -> dict[str, Any]:
    """Run model/tool transitions until a final response is received.

    The returned value must contain the final ``decision`` and an inspectable
    ``trace``. A tool result record preserves the request's ``call_id`` and
    ``name`` and stores the tool output in ``content``.

    This state-transition loop is the human-owned core of iteration 2A.
    """
    loop_turn = 0
    while True:
        response = model(initial_context)
        initial_context.append(response)
        if response["type"] != "tool_call":
            return {"decision": response["decision"], "trace": initial_context}
        tool_name = response["name"]
        if tool_name not in tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        tool_output = tools[tool_name](**response["arguments"])
        initial_context.append(
            {
                "type": "tool_result",
                "call_id": response["call_id"],
                "content": tool_output,
                "name": response["name"],
            }
        )
        loop_turn += 1
        if loop_turn >= max_model_turns:
            raise Exception(f"Max model turns reached, loop turn: {loop_turn}")
