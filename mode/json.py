from __future__ import annotations


def load_json_payload(json_path: str) -> dict[str, object]:
	pass


def normalize_label(label: str) -> str:
	pass


def parse_filter_bank(payload: dict[str, object]) -> dict[int, dict[str, list[list[float]]]]:
	pass


def parse_pattern_cases(payload: dict[str, object]) -> list[dict[str, object]]:
	pass


def validate_case_shape(
	case_id: str,
	pattern: list[list[float]],
	filters_by_label: dict[str, list[list[float]]],
) -> tuple[bool, str | None]:
	pass


def run_json_mode(json_path: str = "data/data.json", epsilon: float = 1e-9, repeat: int = 10) -> dict[str, object]:
	pass

