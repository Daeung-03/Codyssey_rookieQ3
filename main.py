from __future__ import annotations

from typing import Literal


ModeName = Literal["user", "json"]


def select_mode() -> ModeName:
	pass


def run_user_flow() -> None:
	pass


def run_json_flow(json_path: str = "data/data.json") -> None:
	pass


def main() -> None:
	pass

