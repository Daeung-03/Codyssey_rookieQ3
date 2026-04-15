from __future__ import annotations

from typing import Literal

from mode.user import run_user_mode


ModeName = Literal["user", "json"]


def select_mode() -> ModeName:
	while True:
		print("\n실행 모드를 선택하세요.")
		print("1) 사용자 입력(3x3)")
		print("2) data.json 분석")
		selected = input("선택 > ").strip()
		if selected == "1":
			return "user"
		if selected == "2":
			return "json"
		print("입력 오류: 1 또는 2를 입력하세요.")


def run_user_flow() -> None:
	run_user_mode()


def run_json_flow(json_path: str = "data/data.json") -> None:
	pass


def main() -> None:
	mode = select_mode()
	if mode == "user":
		run_user_flow()
		return
	run_json_flow()


if __name__ == "__main__":
	main()

