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

### 1) 프로그램 실행

프로젝트 루트에서 아래 명령으로 실행합니다.

```bash
python3 main.py
```

실행 후 모드를 선택합니다.

- `1`: 사용자 입력 모드 (`3×3` 패턴 직접 입력)
- `2`: JSON 분석 모드 (`data/data.json` 기준 배치 실행)

### 2) data.json 작성 방법 (`patterns`)

JSON 분석 모드(선택 `2`)를 사용하려면 `data/data.json`의 `patterns`를 아래 규칙으로 채웁니다.

- 키 형식: `size_{N}_{idx}`
	- `N`: 패턴의 한 변 길이 (`3`, `5` 등)
	- `idx`: 같은 크기 패턴의 순번 (`1`, `2`, `3` ...)
- 값 형식: 객체(Object)
	- `input`: `N×N` 2차원 배열
	- `expected`: 기대 결과 값

예시:

```json
{
	"patterns": {
		"size_3_1": {
			"input": [
				[1, 0, 1],
				[0, 1, 0],
				[1, 0, 1]
			],
			"expected": "Cross"
		},
		"size_5_1": {
			"input": [
				[1, 0, 0, 0, 1],
				[0, 1, 0, 1, 0],
				[0, 0, 1, 0, 0],
				[0, 1, 0, 1, 0],
				[1, 0, 0, 0, 1]
			],
			"expected": "Cross"
		}
	}
}
```

`patterns`에 들어가는 각 항목은 반드시 `key(size_{N}_{idx})`, `input(2차원 배열)`, `expected`를 포함해야 합니다.

## 결과 리포트

### 1) FAIL이 아닌 경우(매칭 성공) 설명

JSON 분석 모드에서 `PASS`가 되려면 아래 순서를 모두 통과해야 합니다.

1. **expected 정규화(normalization)**
	 - `expected`는 공백/대소문자 무시 후 정규화합니다.
	 - 허용 값:
		 - `Cross`: `"Cross"`, `"cross"`, `"+"`
		 - `X`: `"X"`, `"x"`
	 - 이 외 값은 스키마 오류로 `FAIL(Data_schema)` 처리됩니다.

2. **점수 비교 + 엡실론(epsilon) 정책**
	 - 점수는 MAC으로 `score_cross`, `score_x`를 계산합니다.
	 - 판정식(기본 `epsilon = 1e-9`):
		 - `score_cross + epsilon >= score_x` 이면 `predicted = Cross`
		 - 그 외 `predicted = X`
	 - 즉, 두 점수가 거의 같은 미세 오차 구간에서는 `Cross` 쪽으로 판정됩니다.

3. **최종 성공 조건**
	 - 정규화된 `expected`와 `predicted`가 같으면 `PASS`입니다.

### 2) 우리가 FAIL로 잡아내는 모든 케이스

현재 구현에서 `FAIL`은 아래 3가지 유형으로 분류됩니다.

#### A. `Data_schema` (데이터 형식/구조 문제)

- `patterns` 자체가 객체가 아님
- 케이스 키가 `size_{N}_{idx}` 형식이 아니어서 size 추출 불가
- `patterns.{case}.input`이 2차원 배열 형식이 아님
	- 비어 있음
	- 행이 비어 있음
	- 숫자 변환 실패
	- 행 길이 불일치
	- 정사각 행렬 아님
- `patterns.{case}.expected`가 허용 라벨(`Cross/+`, `X`)이 아님
- `filters` 객체가 없거나, 해당 size 필터를 찾을 수 없음 (`size_{N}` 미존재)
- `filters.size_{N}`가 객체가 아니거나 유효한 필터가 없음
- 필터 라벨이 유효하지 않음 (`Cross/+`, `X` 외)
- `Cross` 또는 `X` 필터 누락
- pattern과 필터 크기 불일치

#### B. `Statics` (통계적 동률/미세 차이 구간 불일치)

- `predicted != expected` 이면서 `|score_cross - score_x| <= epsilon`
- 즉, 점수 차이가 엡실론 이내(거의 동률)인데 기대 라벨과 다를 때 `FAIL(Statics)`

#### C. `Logic` (일반 분류 불일치)

- `predicted != expected` 이면서 `|score_cross - score_x| > epsilon`
- 즉, 동률 구간이 아닌 명확한 점수 차이에서 기대 라벨과 다를 때 `FAIL(Logic)`


