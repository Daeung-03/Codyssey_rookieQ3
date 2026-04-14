from __future__ import annotations


def measure_mac_time_ms(pattern: list[list[float]], filter_kernel: list[list[float]], repeat: int = 10) -> float:
	pass


def benchmark_single_size(
	size: int,
	pattern: list[list[float]],
	filter_kernel: list[list[float]],
	repeat: int = 10,
) -> dict[str, object]:
	pass


def benchmark_sizes(
	cases_by_size: dict[int, tuple[list[list[float]], list[list[float]]]],
	repeat: int = 10,
) -> list[dict[str, object]]:
	pass

