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

