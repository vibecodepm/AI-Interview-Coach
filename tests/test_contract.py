import unittest

from src.backend.evaluation_system import InterviewEvaluator, MockLLMClient


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


if __name__ == "__main__":
    unittest.main()
