from __future__ import annotations


def validate_same_shape(matrix_a: list[list[float]], matrix_b: list[list[float]]) -> bool:
	if not matrix_a or not matrix_b:
		return False
	if len(matrix_a) != len(matrix_b):
		return False
	if any(len(row) != len(matrix_a[0]) for row in matrix_a):
		return False
	if any(len(row) != len(matrix_b[0]) for row in matrix_b):
		return False
	return len(matrix_a[0]) == len(matrix_b[0])


def mac(pattern: list[list[float]], filter_kernel: list[list[float]]) -> float:
	if not validate_same_shape(pattern, filter_kernel):
		raise ValueError("pattern과 filter의 크기가 일치해야 합니다.")
	return sum(
		pattern[row][col] * filter_kernel[row][col]
		for row in range(len(pattern))
		for col in range(len(pattern[row]))
	)


def mac_scores(pattern: list[list[float]], filters_by_label: dict[str, list[list[float]]]) -> dict[str, float]:
	return {
		label: mac(pattern, filter_kernel)
		for label, filter_kernel in filters_by_label.items()
	}

