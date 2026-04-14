# Codyssey_rookieQ3
2026 코디세이 AI 올인원 교육과정 입학연수과정 문제 3번

## 디렉토리 구조

```text
Codyssey_rookieQ3/
├─ main.py                 # 프로그램 진입점 및 실행 모드(user/json) 선택 흐름 담당
├─ Problem.md              # 과제 요구사항 및 기능/평가 기준 명세 문서
├─ README.md               # 프로젝트 개요, 구조, 실행/결과 리포트 문서
├─ core/
│  ├─ mac.py               # 패턴-필터 MAC(Multiply-Accumulate) 핵심 연산 담당
│  ├─ judge.py             # 점수 비교(epsilon), 판정(Cross/X/UNDECIDED), PASS/FAIL 평가 담당
│  └─ performance.py       # 크기별 MAC 연산 시간 측정 및 성능 지표 산출 담당
├─ data/
│  └─ data.json            # JSON 분석 모드에서 사용하는 필터/패턴/expected 테스트 데이터
├─ mode/
│  ├─ user.py              # 3×3 콘솔 입력 파싱/검증 및 사용자 입력 모드 실행 담당
│  └─ json.py              # data.json 로드/스키마 검증/정규화 및 배치 판정 모드 실행 담당
└─ ui/
	└─ ui.py                # 콘솔 출력 포맷(결과/요약/테이블) 관련 UI 레이어 담당
```
