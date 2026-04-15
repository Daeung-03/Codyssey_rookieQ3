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

## 실행 방법

### 1. 클론 후 실행
저장소를 로컬 환경으로 클론한 뒤, 메인 스크립트를 실행하여 프로그램을 시작할 수 있습니다.
```bash
# 1. 저장소 클론
git clone https://github.com/Daeung-03/Codyssey_rookieQ3.git

# 2. 프로젝트 디렉토리로 이동
cd Codyssey_rookieQ3

# 3. 프로그램 실행
python main.py
```

### 2. 사용자 입력 모드 (User mode)
프로그램 실행 후 메뉴에서 `1`을 선택하여 실행합니다.
- 3×3 크기의 두 가지 필터(A, B)와 판정할 패턴을 콘솔에서 직접 입력합니다.
- 숫자는 한 줄씩 **공백으로 구분하여** 3줄씩 입력합니다.
- 입력이 완료되면 두 필터에 대한 패턴의 MAC 연산 점수(유사도), 연산 시간, 그리고 최종 판정 결과(A, B 또는 UNDECIDED)를 출력합니다.

### 3. JSON 분석 모드 (JSON mode)
프로그램 실행 후 메뉴에서 `2`를 선택하여 실행합니다.
- `data/data.json` 파일을 로드하여 5×5, 13×13, 25×25 등 다양한 크기의 테스트 데이터들에 대해 일괄적으로 MAC 연산과 판정을 수행합니다.
- 내부적으로 크로스(Cross)와 X 패턴에 대한 정규화(`+` → `Cross`, `x` → `X`)가 이루어지며, 동점 확인을 위해 epsilon 오차 범위 처리가 진행됩니다.
- 실행이 완료되면 크기별 평균 연산 시간과 연산 횟수(N²) 성능 리포트, 그리고 전체 PASS/FAIL 테스트 요약을 출력합니다.

```