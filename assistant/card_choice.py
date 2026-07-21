"""Offline card-choice policy scaffold."""

from typing import Any


def choose_card(observation: dict[str, Any]) -> dict[str, str]:
    """Return one legal card id (or ``skip``) and a non-empty reason.

    Legal card ids come only from ``observation["offered_cards"]``. The
    special ``skip`` action is legal only when ``observation["can_skip"]`` is
    true. This function must be deterministic for the same observation.

    This decision policy is the human-owned core of iteration 1A.
    """
    deck_summary = observation["deck_summary"]
    choices = observation["offered_cards"]
    can_skip = observation["can_skip"]
    if not choices or len(choices) == 0:
        if can_skip:
            return {"choice": "skip", "reason": "选择仅有跳过选项"}
        raise ValueError("No legal actions")

    if deck_summary is None or not isinstance(deck_summary, dict):
        raise ValueError("deck_summary is not a dict")
    attack_count =  int(deck_summary["attack_cards"]) if deck_summary["attack_cards"] else 0
    skill_count = int(deck_summary["skill_cards"]) if deck_summary["skill_cards"] else 0
    strike_count = int(deck_summary["cards_containing_strike"]) if deck_summary["cards_containing_strike"] else 0
    prefer_skill_card = False
    if attack_count - strike_count / 2 > skill_count:
        prefer_skill_card = True
    pick_card = {"choice": choices[0]["id"], "reason": "默认第一个选择"}
    for choice in choices:
        if prefer_skill_card and choice["type"] == "skill":
            skill_count += 1
            pick_card = {"choice": choice["id"], "reason": "攻击卡过多，优先选择技能卡"}
            break
        else:
            attack_count += 1
            pick_card = {"choice": choice["id"], "reason": "优先选择攻击牌"}
            break
    if can_skip and attack_count > skill_count * 2 and not pick_card["choice"] == "attack":
        pick_card = {"choice": "skip", "reason": "攻击卡过多，选择跳过"}
    return pick_card
