from __future__ import annotations


def decide_label(score_cross: float, score_x: float, epsilon: float = 1e-9) -> str:
	pass


def normalize_expected_label(expected: str) -> str:
	pass


def evaluate_prediction(predicted: str, expected: str) -> bool:
	pass


def build_case_result(
	case_id: str,
	score_cross: float,
	score_x: float,
	predicted: str,
	expected: str | None,
	reason: str | None = None,
) -> dict[str, object]:
	pass

