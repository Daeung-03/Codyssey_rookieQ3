from __future__ import annotations


def decide_label(score_cross: float, score_x: float, epsilon: float = 1e-9) -> str:
	if abs(score_cross - score_x) < epsilon:
		return "UNDECIDED"
	return "Cross" if score_cross > score_x else "X"


def normalize_expected_label(expected: str) -> str:
	raw = expected.strip().lower()
	if raw in {"+", "cross"}:
		return "Cross"
	if raw in {"x"}:
		return "X"
	if raw in {"undecided", "un_decided", "un-decided"}:
		return "UNDECIDED"
	raise ValueError(f"지원하지 않는 라벨입니다: {expected}")


def evaluate_prediction(predicted: str, expected: str) -> bool:
	return predicted == normalize_expected_label(expected)


def build_case_result(
	case_id: str,
	score_cross: float,
	score_x: float,
	predicted: str,
	expected: str | None,
	reason: str | None = None,
) -> dict[str, object]:
	is_pass = False if expected is None else predicted == expected
	return {
		"case_id": case_id,
		"score_cross": score_cross,
		"score_x": score_x,
		"predicted": predicted,
		"expected": expected,
		"status": "PASS" if is_pass else "FAIL",
		"pass": is_pass,
		"reason": reason,
	}

