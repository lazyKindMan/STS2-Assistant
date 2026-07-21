import json
import unittest
from pathlib import Path

from assistant.card_choice import choose_card


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "ironclad_card_reward.json"


class ChooseCardTest(unittest.TestCase):
    def test_returns_the_same_legal_decision_with_a_reason(self) -> None:
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        observation = fixture["observation"]

        first_decision = choose_card(observation)
        second_decision = choose_card(observation)

        legal_choices = {card["id"] for card in observation["offered_cards"]}
        if observation["can_skip"]:
            legal_choices.add("skip")

        self.assertEqual(first_decision, second_decision)
        self.assertIsInstance(first_decision, dict)
        self.assertIn(first_decision["choice"], legal_choices)
        self.assertTrue(first_decision["reason"].strip())


if __name__ == "__main__":
    unittest.main()
