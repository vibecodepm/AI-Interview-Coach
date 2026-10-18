import unittest

from src.backend.evaluation_system import AnswerScoreSchema, InterviewEvaluator, MockLLMClient


class CapturingLLMClient(MockLLMClient):
    def __init__(self):
        self.last_prompt = ""

    def call_structured(self, prompt, target_schema):
        self.last_prompt = prompt
        return super().call_structured(prompt, target_schema)


class UnsafeRewriteLLMClient(MockLLMClient):
    def call_structured(self, prompt, target_schema):
        result = super().call_structured(prompt, target_schema)
        if target_schema is not list:
            result.improved_answer_rewrite = "The result improved retention by 42% in 2025."
        return result


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.engine = InterviewEvaluator(MockLLMClient())

    def test_question_contract_has_stable_ids(self):
        questions = self.engine.generate_questions(
            "Product manager with payments experience",
            "Own a digital wallet product",
            "AI Product Manager",
        )
        self.assertEqual(len(questions), 3)
        self.assertEqual([question.question_id for question in questions], ["q1", "q2", "q3"])

    def test_insufficient_answer_is_zero_and_low_confidence(self):
        result = self.engine.score_answer("Describe a product decision.", "abc", "", "", "PM")
        self.assertEqual(result.overall_score, 0)
        self.assertEqual(result.confidence, "low")
        self.assertEqual(len(result.detailed_scores), 4)

    def test_complete_answer_matches_frontend_score_contract(self):
        result = self.engine.score_answer(
            "Describe a product decision.",
            "I analyzed customer data, aligned engineering, and launched a change that improved retention by 20 percent.",
            "",
            "",
            "PM",
        )
        self.assertGreater(result.overall_score, 0)
        self.assertEqual(len(result.detailed_scores), 4)
        self.assertIsNotNone(result.feedback.improvements)

    def test_coaching_prompt_requires_evidence_grounded_rewrite(self):
        client = CapturingLLMClient()
        evaluator = InterviewEvaluator(client)
        result = evaluator.score_answer(
            "Tell me about a difficult product decision.",
            "I reviewed support tickets, aligned engineering, and changed the roadmap.",
            "",
            "",
            "PM",
        )

        self.assertIsInstance(result, AnswerScoreSchema)
        self.assertIn("Never invent metrics", client.last_prompt)
        self.assertIn("bracketed prompt", client.last_prompt)
        self.assertIn("preserve the candidate's facts", client.last_prompt)

    def test_rewrite_safety_replaces_unsupported_numeric_claims(self):
        evaluator = InterviewEvaluator(UnsafeRewriteLLMClient())
        result = evaluator.score_answer(
            "Describe a product decision.",
            "I reviewed customer feedback and changed the roadmap.",
            "",
            "",
            "PM",
        )

        self.assertNotIn("42%", result.improved_answer_rewrite)
        self.assertNotIn("2025", result.improved_answer_rewrite)
        self.assertIn("[the missing metric or outcome]", result.improved_answer_rewrite)


if __name__ == "__main__":
    unittest.main()
