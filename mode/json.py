from __future__ import annotations

import json
import re

from core.judge import build_case_result, decide_label, normalize_expected_label
from core.mac import mac_scores, validate_same_shape
from core.performance import benchmark_sizes


def load_json_payload(json_path: str) -> dict[str, object]:
	try:
		with open(json_path, "r", encoding="utf-8") as file:
			payload = json.load(file)
	except FileNotFoundError as error:
		raise ValueError(f"JSON 파일을 찾을 수 없습니다: {json_path}") from error
	except json.JSONDecodeError as error:
		raise ValueError(f"JSON 파싱 실패: {error}") from error
	if not isinstance(payload, dict):
		raise ValueError("최상위 JSON 구조는 객체(dict)여야 합니다.")
	return payload


def normalize_label(label: str) -> str:
	raw = label.strip().lower()
	if raw in {"cross", "+"}:
		return "Cross"
	if raw in {"x"}:
		return "X"
	raise ValueError(f"지원하지 않는 라벨입니다: {label}")


def _to_float_matrix(raw_matrix: object, matrix_name: str) -> list[list[float]]:
	if not isinstance(raw_matrix, list) or not raw_matrix:
		raise ValueError(f"{matrix_name}: 2차원 배열이 필요합니다.")
	matrix: list[list[float]] = []
	for row in raw_matrix:
		if not isinstance(row, list) or not row:
			raise ValueError(f"{matrix_name}: 각 행은 비어있지 않은 배열이어야 합니다.")
		try:
			matrix.append([float(value) for value in row])
		except (TypeError, ValueError) as error:
			raise ValueError(f"{matrix_name}: 숫자 변환 실패") from error
	width = len(matrix[0])
	if any(len(row) != width for row in matrix):
		raise ValueError(f"{matrix_name}: 행 길이가 일치해야 합니다.")
	if len(matrix) != width:
		raise ValueError(f"{matrix_name}: 정사각 행렬이어야 합니다.")
	return matrix


def parse_filter_bank(payload: dict[str, object]) -> dict[int, dict[str, list[list[float]]]]:
	raw_filters = payload.get("filters")
	if not isinstance(raw_filters, dict):
		raise ValueError("filters 객체가 필요합니다.")

	result: dict[int, dict[str, list[list[float]]]] = {}
	for size_key, filter_group in raw_filters.items():
		if not isinstance(size_key, str):
			continue
		match = re.match(r"^size_(\d+)$", size_key)
		if match is None:
			continue
		size = int(match.group(1))
		if not isinstance(filter_group, dict):
			raise ValueError(f"filters.{size_key}는 객체여야 합니다.")
		normalized_group: dict[str, list[list[float]]] = {}
		for label_key, matrix in filter_group.items():
			label = normalize_label(str(label_key))
			normalized_group[label] = _to_float_matrix(matrix, f"filters.{size_key}.{label_key}")
		result[size] = normalized_group

	if not result:
		raise ValueError("유효한 filter(size_N)가 없습니다.")
	return result


def parse_pattern_cases(payload: dict[str, object]) -> list[dict[str, object]]:
	raw_patterns = payload.get("patterns")
	if not isinstance(raw_patterns, dict):
		raise ValueError("patterns 객체가 필요합니다.")

	cases: list[dict[str, object]] = []
	for case_id, item in raw_patterns.items():
		if not isinstance(case_id, str) or not isinstance(item, dict):
			continue
		match = re.match(r"^size_(\d+)_", case_id)
		if match is None:
			cases.append(
				{
					"case_id": case_id,
					"size": None,
					"pattern": None,
					"expected": None,
					"reason": "케이스 키에서 size를 추출할 수 없습니다.",
				}
			)
			continue
		size = int(match.group(1))
		try:
			pattern = _to_float_matrix(item.get("input"), f"patterns.{case_id}.input")
			expected = normalize_expected_label(str(item.get("expected", "")))
			cases.append(
				{
					"case_id": case_id,
					"size": size,
					"pattern": pattern,
					"expected": expected,
					"reason": None,
				}
			)
		except ValueError as error:
			cases.append(
				{
					"case_id": case_id,
					"size": size,
					"pattern": None,
					"expected": None,
					"reason": str(error),
				}
			)

	return cases


def validate_case_shape(
	case_id: str,
	pattern: list[list[float]],
	filters_by_label: dict[str, list[list[float]]],
) -> tuple[bool, str | None]:
	if not pattern or any(len(row) != len(pattern) for row in pattern):
		return False, f"{case_id}: pattern이 정사각 행렬이 아닙니다."
	for label in ("Cross", "X"):
		if label not in filters_by_label:
			return False, f"{case_id}: {label} 필터가 없습니다."
		if not validate_same_shape(pattern, filters_by_label[label]):
			return False, f"{case_id}: pattern과 {label} 필터 크기가 일치하지 않습니다."
	return True, None


def run_json_mode(json_path: str = "data/data.json", epsilon: float = 1e-9, repeat: int = 10) -> dict[str, object]:
	payload = load_json_payload(json_path)
	filter_bank = parse_filter_bank(payload)
	cases = parse_pattern_cases(payload)

	print("\n=== data.json 분석 모드 ===")
	case_results: list[dict[str, object]] = []
	first_case_by_size: dict[int, tuple[list[list[float]], list[list[float]]]] = {}

	for case in cases:
		case_id = str(case["case_id"])
		size = case.get("size")
		pattern = case.get("pattern")
		expected = case.get("expected")
		case_reason = case.get("reason")

		if case_reason is not None:
			result = build_case_result(case_id, 0.0, 0.0, "UNDECIDED", None, str(case_reason))
			case_results.append(result)
			print(f"{case_id} | FAIL | reason={case_reason}")
			continue

		if not isinstance(size, int) or size not in filter_bank:
			reason = f"{case_id}: size_{size} 필터를 찾을 수 없습니다."
			result = build_case_result(case_id, 0.0, 0.0, "UNDECIDED", expected if isinstance(expected, str) else None, reason)
			case_results.append(result)
			print(f"{case_id} | FAIL | reason={reason}")
			continue

		if not isinstance(pattern, list):
			reason = f"{case_id}: pattern 데이터가 없습니다."
			result = build_case_result(case_id, 0.0, 0.0, "UNDECIDED", expected if isinstance(expected, str) else None, reason)
			case_results.append(result)
			print(f"{case_id} | FAIL | reason={reason}")
			continue

		filters_by_label = filter_bank[size]
		is_valid, reason = validate_case_shape(case_id, pattern, filters_by_label)
		if not is_valid:
			result = build_case_result(case_id, 0.0, 0.0, "UNDECIDED", expected if isinstance(expected, str) else None, reason)
			case_results.append(result)
			print(f"{case_id} | FAIL | reason={reason}")
			continue

		scores = mac_scores(pattern, {"Cross": filters_by_label["Cross"], "X": filters_by_label["X"]})
		predicted = decide_label(scores["Cross"], scores["X"], epsilon)
		result = build_case_result(
			case_id=case_id,
			score_cross=scores["Cross"],
			score_x=scores["X"],
			predicted=predicted,
			expected=expected if isinstance(expected, str) else None,
		)
		case_results.append(result)

		if size not in first_case_by_size:
			first_case_by_size[size] = (pattern, filters_by_label["Cross"])

		print(
			f"{case_id} | Cross={scores['Cross']:.6f} | X={scores['X']:.6f} | "
			f"pred={predicted} | expected={result['expected']} | {result['status']}"
		)

	total_count = len(case_results)
	pass_count = sum(1 for item in case_results if bool(item["pass"]))
	fail_count = total_count - pass_count

	failures = [
		{"case_id": item["case_id"], "reason": item["reason"] or "예측값과 expected 불일치"}
		for item in case_results
		if not bool(item["pass"])
	]

	if 3 not in first_case_by_size:
		synthetic_pattern = [[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 1.0]]
		synthetic_filter = [[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 1.0]]
		first_case_by_size[3] = (synthetic_pattern, synthetic_filter)

	performance_rows = benchmark_sizes(first_case_by_size, repeat)

	print("\n=== 성능 분석 (MAC 평균, ms) ===")
	print("크기(NxN) | 평균 시간(ms) | 연산 횟수(N^2)")
	for row in performance_rows:
		print(f"{row['size']}x{row['size']} | {row['avg_time_ms']:.6f} | {row['operations']}")

	print("\n=== 결과 요약 ===")
	print(f"총 {total_count}건 | PASS {pass_count}건 | FAIL {fail_count}건")
	if failures:
		print("실패 케이스 목록:")
		for failure in failures:
			print(f"- {failure['case_id']}: {failure['reason']}")

	return {
		"mode": "json",
		"total": total_count,
		"pass": pass_count,
		"fail": fail_count,
		"cases": case_results,
		"failures": failures,
		"performance": performance_rows,
	}

