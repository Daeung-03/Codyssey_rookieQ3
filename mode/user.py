from __future__ import annotations

import math

from core.mac import mac
from core.performance import measure_mac_time_ms


def parse_numeric_row(raw: str, expected_size: int) -> list[float]:
	parts = raw.strip().split()
	if len(parts) != expected_size:
		raise ValueError(f"각 줄에 {expected_size}개의 숫자를 공백으로 입력하세요.")
	try:
		values = [float(value) for value in parts]
	except ValueError as error:
		raise ValueError("숫자만 입력하세요.") from error
	if any(not math.isfinite(value) for value in values):
		raise ValueError("NaN 또는 Inf는 입력할 수 없습니다.")
	return values


def parse_binary_row(raw: str, expected_size: int) -> list[float]:
	values = parse_numeric_row(raw, expected_size)
	if any(value not in (0.0, 1.0) for value in values):
		raise ValueError("패턴은 0 또는 1만 입력할 수 있습니다.")
	return values


def read_square_matrix_from_console(title: str, size: int) -> list[list[float]]:
	print(f"\n{title}")
	matrix: list[list[float]] = []
	row_index = 0
	while row_index < size:
		raw = input(f"{row_index + 1}/{size}행 > ")
		try:
			matrix.append(parse_numeric_row(raw, size))
			row_index += 1
		except ValueError as error:
			print(f"입력 형식 오류: {error}")
	return matrix


def read_binary_square_matrix_from_console(title: str, size: int) -> list[list[float]]:
	print(f"\n{title}")
	matrix: list[list[float]] = []
	row_index = 0
	while row_index < size:
		raw = input(f"{row_index + 1}/{size}행 > ")
		try:
			matrix.append(parse_binary_row(raw, size))
			row_index += 1
		except ValueError as error:
			print(f"입력 형식 오류: {error}")
	return matrix


def read_user_inputs(size: int = 3) -> tuple[list[list[float]], list[list[float]], list[list[float]]]:
	if size != 3:
		raise ValueError("현재 user 모드는 3x3만 지원합니다.")
	filter_a = read_square_matrix_from_console("3x3 필터 A를 입력하세요.", size)
	filter_b = read_square_matrix_from_console("3x3 필터 B를 입력하세요.", size)
	pattern = read_binary_square_matrix_from_console("3x3 패턴을 입력하세요. (0 또는 1)", size)
	return filter_a, filter_b, pattern


def run_user_mode(size: int = 3, repeat: int = 10) -> dict[str, object]:
	filter_a, filter_b, pattern = read_user_inputs(size)
	score_a = mac(pattern, filter_a)
	score_b = mac(pattern, filter_b)
	decision = "A" if score_a >= score_b else "B"
	a_time_ms = measure_mac_time_ms(pattern, filter_a, repeat)
	b_time_ms = measure_mac_time_ms(pattern, filter_b, repeat)

	print("\n=== user mode 결과 ===")
	print(f"A 점수: {score_a:.6f} | 평균 시간: {a_time_ms:.6f}ms")
	print(f"B 점수: {score_b:.6f} | 평균 시간: {b_time_ms:.6f}ms")
	print(f"분류: 패턴 {decision}")

	return {
		"mode": "user",
		"score_a": score_a,
		"score_b": score_b,
		"decision": decision,
		"avg_time_ms": {"A": a_time_ms, "B": b_time_ms},
	}

