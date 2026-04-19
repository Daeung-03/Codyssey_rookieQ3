from __future__ import annotations

from time import perf_counter

from core.mac import mac


def measure_mac_time_ms(pattern: list[list[float]], filter_kernel: list[list[float]], repeat: int = 10) -> float:
	if repeat <= 0:
		raise ValueError("repeat는 1 이상이어야 합니다.")
	start = perf_counter()
	for _ in range(repeat):
		mac(pattern, filter_kernel)
	elapsed_s = perf_counter() - start
	return (elapsed_s * 1000) / repeat


def benchmark_single_size(
	size: int,
	pattern: list[list[float]],
	filter_kernel: list[list[float]],
	repeat: int = 10,
) -> dict[str, object]:
	return {
		"size": size,
		"avg_time_ms": measure_mac_time_ms(pattern, filter_kernel, repeat),
		"operations": size * size,
	}


def benchmark_sizes(
	cases_by_size: dict[int, tuple[list[list[float]], list[list[float]]]],
	repeat: int = 10,
) -> list[dict[str, object]]:
	results: list[dict[str, object]] = []
	for size in sorted(cases_by_size):
		pattern, filter_kernel = cases_by_size[size]
		results.append(benchmark_single_size(size, pattern, filter_kernel, repeat))
	return results


def build_synthetic_case(size: int) -> tuple[list[list[float]], list[list[float]]]:
	if size <= 0:
		raise ValueError("size는 1 이상이어야 합니다.")
	pattern = [[1.0 for _ in range(size)] for _ in range(size)]
	filter_kernel = [[1.0 for _ in range(size)] for _ in range(size)]
	return pattern, filter_kernel


def benchmark_synthetic_sizes(sizes: list[int], repeat: int = 10) -> list[dict[str, object]]:
	if not sizes:
		return []

	results: list[dict[str, object]] = []
	for size in sorted(sizes):
		pattern, filter_kernel = build_synthetic_case(size)
		avg_time_ms = measure_mac_time_ms(pattern, filter_kernel, repeat)
		operations = size * size
		results.append(
			{
				"size": size,
				"avg_time_ms": avg_time_ms,
				"operations": operations,
			}
		)

	for index in range(1, len(results)):
		current = results[index]
		previous = results[index - 1]
		time_ratio = float(current["avg_time_ms"]) / float(previous["avg_time_ms"])
		current["time_ratio_from_prev"] = time_ratio

	results[0]["time_ratio_from_prev"] = None

	return results

