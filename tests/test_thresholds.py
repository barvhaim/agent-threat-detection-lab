from agent_threat_detection.benchmark.thresholds import select_operating_threshold


def test_threshold_selection_respects_precision_floor_then_maximizes_recall():
    labels = [1, 1, 1, 0, 0, 0]
    scores = [0.95, 0.82, 0.61, 0.58, 0.20, 0.05]

    selection = select_operating_threshold(labels, scores, precision_floor=0.90)

    assert selection.threshold > 0.58
    assert selection.precision >= 0.90
    assert selection.recall == 1.0


def test_threshold_selector_reports_review_rate():
    selection = select_operating_threshold(
        [1, 0, 1, 0],
        [0.9, 0.7, 0.55, 0.1],
        precision_floor=0.5,
        abstain_margin=0.1,
    )

    assert 0.0 <= selection.review_rate <= 1.0
