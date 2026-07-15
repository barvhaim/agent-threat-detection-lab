import unittest

from agent_threat_detection.evaluation.metrics import evaluate_binary_records


class BinaryMetricsTest(unittest.TestCase):
    def test_computes_confusion_counts_and_metrics(self):
        expected = {
            "a": True,
            "b": True,
            "c": False,
            "d": False,
        }
        predicted = {
            "a": True,
            "b": False,
            "c": True,
            "d": False,
        }

        result = evaluate_binary_records(expected, predicted)

        self.assertEqual((result.tp, result.fp, result.fn, result.tn), (1, 1, 1, 1))
        self.assertEqual(result.precision, 0.5)
        self.assertEqual(result.recall, 0.5)
        self.assertEqual(result.f1, 0.5)

    def test_missing_predictions_are_counted_as_negative(self):
        result = evaluate_binary_records({"attack": True, "safe": False}, {"safe": False})

        self.assertEqual(result.fn, 1)
        self.assertEqual(result.missing_prediction_ids, ("attack",))

    def test_unexpected_predictions_are_reported_but_not_scored(self):
        result = evaluate_binary_records({"safe": False}, {"safe": False, "extra": True})

        self.assertEqual(result.tn, 1)
        self.assertEqual(result.unexpected_prediction_ids, ("extra",))


if __name__ == "__main__":
    unittest.main()
