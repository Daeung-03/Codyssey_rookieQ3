from __future__ import annotations

from time import perf_counter


def parse_numeric_row(raw: str, expected_size: int) -> list[float]:
	parts = raw.strip().split()
	if len(parts) != expected_size:
		raise ValueError(f"각 줄에 {expected_size}개의 숫자를 공백으로 입력하세요.")
	try:
		return [float(value) for value in parts]
	except ValueError as error:
		raise ValueError("숫자만 입력하세요.") from error


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


def read_user_inputs(size: int = 3) -> tuple[list[list[float]], list[list[float]], list[list[float]]]:
	if size != 3:
		raise ValueError("현재 user 모드는 3x3만 지원합니다.")
	filter_a = read_square_matrix_from_console("3x3 필터 A를 입력하세요.", size)
	filter_b = read_square_matrix_from_console("3x3 필터 B를 입력하세요.", size)
	pattern = read_square_matrix_from_console("3x3 패턴을 입력하세요.", size)
	return filter_a, filter_b, pattern


def _mac(pattern: list[list[float]], filter_kernel: list[list[float]]) -> float:
	return sum(
		pattern[row][col] * filter_kernel[row][col]
		for row in range(len(pattern))
		for col in range(len(pattern[row]))
	)


def _judge(score_a: float, score_b: float, epsilon: float) -> str:
	if abs(score_a - score_b) < epsilon:
		return "판정불가"
	return "A" if score_a > score_b else "B"


def _measure_avg_time_ms(
	pattern: list[list[float]],
	filter_kernel: list[list[float]],
	repeat: int,
) -> float:
	start = perf_counter()
	for _ in range(repeat):
		_mac(pattern, filter_kernel)
	elapsed_s = perf_counter() - start
	return (elapsed_s * 1000) / repeat


def run_user_mode(size: int = 3, epsilon: float = 1e-9, repeat: int = 10) -> dict[str, object]:
	filter_a, filter_b, pattern = read_user_inputs(size)
	score_a = _mac(pattern, filter_a)
	score_b = _mac(pattern, filter_b)
	decision = _judge(score_a, score_b, epsilon)
	a_time_ms = _measure_avg_time_ms(pattern, filter_a, repeat)
	b_time_ms = _measure_avg_time_ms(pattern, filter_b, repeat)

	print("\n=== user mode 결과 ===")
	print(f"A 점수: {score_a:.6f} | 평균 시간: {a_time_ms:.6f}ms")
	print(f"B 점수: {score_b:.6f} | 평균 시간: {b_time_ms:.6f}ms")
	print(f"판정: {decision}")

	return {
		"mode": "user",
		"score_a": score_a,
		"score_b": score_b,
		"decision": decision,
		"avg_time_ms": {"A": a_time_ms, "B": b_time_ms},
	}

