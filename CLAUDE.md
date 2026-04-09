# Mini NPU Simulator — Claude Code 프로젝트 가이드

## 1. 프로젝트 개요

MAC(Multiply-Accumulate) 연산으로 패턴을 판별하는 Python 콘솔 애플리케이션.
모드 1(사용자 입력 3×3)과 모드 2(data.json 분석 5×5/13×13/25×25)를 지원한다.
- 상세 요구사항: `docs/MISSION.md`
- 구현 로드맵: `docs/ROADMAP.md`

## 2. 절대 규칙

1. **Python 3.8+** 호환 (walrus operator 등 3.8 미지원 구문 금지)
2. **외부 라이브러리 금지** — import는 `json`, `time`, `math` 등 표준 라이브러리만
3. **MAC 연산은 반복문(for)으로 직접 구현** — NumPy 등 벡터화 금지
4. **소스 코드는 `main.py` 단일 파일**에 작성
5. **점수 비교는 epsilon 기반** — `abs(a - b) < 1e-9`이면 동점
6. **인간이 이해하기 쉬운 코드** — 변수명은 의미를 명확히 드러내고, 한 함수는 하나의 역할만 수행하며, 복잡한 로직에는 "왜 이렇게 하는지" 주석을 단다. 영리한 코드보다 명확한 코드를 우선한다
7. **git commit 금지** — 커밋은 사용자가 직접 수행한다

## 3. 프로젝트 구조

```
E1-3/
  main.py          -- 유일한 실행 파일, 전체 로직 포함 (미생성)
  data.json        -- 모드 2용 테스트 데이터 (미생성)
  README.md        -- 실행 방법 + 결과 리포트 (미생성)
  CLAUDE.md        -- 이 파일
  docs/
    MISSION.md     -- 미션 요구사항 원문
    ROADMAP.md     -- 7-Phase 구현 로드맵
```

## 4. 로드맵 작업 지침

- Phase 순서: **1(기반) → 2(MAC 로직) → 3(모드1) → 4(모드2) → 5(성능/리포트) → 6(보너스, 선택) → 7(문서화)**
- 작업 시작 전 `docs/ROADMAP.md`에서 해당 Phase의 **작업 순서**와 **달성 판단 조건**을 읽는다
- 모든 달성 판단 조건을 충족한 후에만 다음 Phase로 진행한다
- Phase 6(보너스)은 사용자가 명시적으로 요청할 때만 진행한다
- **현재 진행 상태: Phase 3 완료 → Phase 4 시작 전**

## 5. 코딩 컨벤션

- **언어**: 주석, 출력 메시지 모두 한국어
- **변수/함수명**: snake_case (`mac_operation`, `normalize_label`, `compare_scores`)
- **상수**: UPPER_SNAKE_CASE (`EPSILON = 1e-9`)
- **출력 형식**: MISSION.md 섹션 9 예시를 따름 (구분선 `#---`, 섹션 번호 `[1]`, `[2]`)
- **에러 처리**: 프로그램 중단 없이 한국어 안내 메시지 출력 후 재입력 유도 또는 케이스 단위 FAIL
- **타입 힌트**: Python 3.8 호환 범위 내 사용 (`typing.List` 등)

## 6. 핵심 도메인 용어

| 용어 | 정의 | 코드 표현 |
|------|------|----------|
| MAC 연산 | 두 n×n 배열의 위치별 곱셈 후 합산 | `mac_operation()` |
| 필터(Filter) | 패턴 판별 기준 배열 | `filter_` (내장 filter와 구분) |
| 패턴(Pattern) | 판별 대상 입력 배열 | `pattern` |
| 표준 라벨 | `"Cross"` 또는 `"X"` (대소문자 정확히) | 문자열 그대로 사용 |
| 라벨 정규화 | `'+'`→`Cross`, `'x'`→`X`, `'cross'`→`Cross` | `normalize_label()` |
| UNDECIDED | 두 점수가 epsilon 이내 동점 | `"UNDECIDED"` |
| epsilon | 부동소수점 비교 허용 오차 | `EPSILON = 1e-9` |

## 7. 작업 워크플로우

각 Phase 작업 시 아래 순서를 반드시 따른다:

1. **플랜 & 설계**: ROADMAP.md를 읽고 구현 계획/설계를 먼저 수립하여 사용자와 공유한다. 코드 작성 전에 "무엇을 왜 어떻게" 합의한다
2. **구현**: 합의된 설계에 따라 코드를 작성한다
3. **설명**: 사용자가 직접 설명할 수 있는 수준으로 충분히 설명한다 — 구조 선택 이유, 함수 역할, 핵심 로직 동작 원리 포함
4. **자체 검증**: 달성 판단 조건을 하나씩 확인한다
5. **CLAUDE.md 상태 업데이트**: 현재 진행 상태를 갱신한다
6. **사용자 보고**: 완료 결과를 보고하고 다음 Phase 진행 여부를 확인한다

- 사용자 확인 없이 Phase 건너뛰기 금지
- git commit은 사용자가 직접 수행 — Claude Code는 절대 커밋하지 않는다

## 8. 검증 명령어

```bash
python main.py                                          # 전체 실행 (모드 선택 화면)
python -c "import main"                                 # import 에러 확인
python -c "import json; json.load(open('data.json'))"   # data.json 파싱 확인
```
