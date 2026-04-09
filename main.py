# main.py — Mini NPU Simulator

import time  # 연산 시간 측정용
from typing import List  # Python 3.8 호환성 지원을 위해 사용 (3.9+에서는 내장 list로 대체 가능)

EPSILON = 1e-9  # 부동소수점 비교 허용 오차


def create_grid(n: int, default_value: float = 0.0) -> List[List[float]]:
    """n×n 크기의 2D 배열을 생성하여 반환한다."""
    return [[default_value] * n for _ in range(n)]


def get_value(grid: List[List[float]], row: int, col: int) -> float:
    """2D 배열의 (row, col) 위치 값을 읽는다."""
    return grid[row][col]


def set_value(grid: List[List[float]], row: int, col: int, value: float) -> None:
    """2D 배열의 (row, col) 위치에 값을 저장한다."""
    grid[row][col] = value


# === Phase 2: MAC 연산 및 점수 비교 핵심 로직 ===


def mac_operation(grid_a: List[List[float]], grid_b: List[List[float]]) -> float:
    """두 n×n 2D 배열의 위치별 곱셈 후 전체 합산(MAC 연산)을 수행한다."""
    n = len(grid_a)
    result = 0.0
    for row in range(n):
        for col in range(n):
            result += grid_a[row][col] * grid_b[row][col]
    return result


def normalize_label(raw: str) -> str:
    """원본 라벨을 표준 라벨('Cross' 또는 'X')로 정규화한다.

    expected 값('+', 'x')과 filter 키('cross', 'x') 모두 처리한다.
    매핑에 없는 값은 원본을 그대로 반환한다.
    """
    mapping = {
        "+": "Cross",
        "cross": "Cross",
        "x": "X",
    }
    key = raw.strip().lower()
    if key in mapping:
        return mapping[key]
    return raw


def compare_scores(cross_score: float, x_score: float) -> str:
    """두 필터 점수를 epsilon 기반으로 비교하여 판정 결과를 반환한다.

    차이가 EPSILON 미만이면 'UNDECIDED', 아니면 높은 쪽의 라벨을 반환한다.
    """
    if abs(cross_score - x_score) < EPSILON:
        return "UNDECIDED"
    if cross_score > x_score:
        return "Cross"
    return "X"


def judge_result(verdict: str, expected: str) -> str:
    """판정 결과와 정규화된 기대 라벨을 비교하여 PASS 또는 FAIL을 반환한다."""
    if verdict == expected:
        return "PASS"
    return "FAIL"


# === Phase 3: 모드 1 — 사용자 입력 (3×3) ===


def validate_row(raw: str, expected_cols: int) -> List[float]:
    """한 줄의 입력 문자열을 검증하고 파싱한다.

    열 수 불일치 또는 숫자 파싱 실패 시 ValueError를 발생시킨다.
    """
    tokens = raw.strip().split()
    if len(tokens) != expected_cols:
        raise ValueError(
            f"입력 형식 오류: 각 줄에 {expected_cols}개의 숫자를 공백으로 구분해 입력하세요."
        )
    values = []
    for token in tokens:
        try:
            values.append(float(token))
        except ValueError:
            raise ValueError(
                "입력 형식 오류: 숫자가 아닌 값이 포함되어 있습니다. 다시 입력하세요."
            )
    return values


def input_grid(n: int, label: str) -> List[List[float]]:
    """n줄을 입력받아 n×n 2D 배열을 생성하여 반환한다.

    검증 실패 시 그리드 전체를 처음부터 재입력받는다.
    """
    while True:
        print(f"{label} ({n}줄 입력, 공백 구분)")
        grid = []
        valid = True
        for _ in range(n):
            raw = input()
            try:
                row = validate_row(raw, n)
                grid.append(row)
            except ValueError as e:
                print(e)
                valid = False
                break
        if valid:
            return grid
        # 검증 실패 시 while 루프 처음으로 돌아가 전체 재입력


def compare_scores_ab(score_a: float, score_b: float) -> str:
    """두 필터 점수를 epsilon 기반으로 비교하여 A/B/UNDECIDED를 반환한다.

    모드 1 전용: 임의의 필터 A, B에 대한 판정 결과를 반환한다.
    """
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    if score_a > score_b:
        return "A"
    return "B"


def measure_mac_time(
    grid_a: List[List[float]], grid_b: List[List[float]], repeat: int = 10
) -> float:
    """MAC 연산을 repeat회 반복 실행하고 평균 시간을 ms 단위로 반환한다.

    I/O를 제외하고 연산 함수 호출 구간만 측정한다.
    """
    start = time.perf_counter()
    for _ in range(repeat):
        mac_operation(grid_a, grid_b)
    end = time.perf_counter()
    avg_ms = (end - start) / repeat * 1000
    return avg_ms


def show_menu() -> str:
    """모드 선택 메뉴를 출력하고 유효한 선택('1' 또는 '2')을 반환한다."""
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print()
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    while True:
        choice = input("선택: ").strip()
        if choice in ("1", "2"):
            return choice
        print("올바른 번호를 입력하세요 (1 또는 2).")


def run_mode_1() -> None:
    """모드 1 전체 실행 흐름: 필터 입력 → 패턴 입력 → MAC 연산 → 결과 출력."""
    # [1] 필터 입력
    print()
    print("#----------------------------------------")
    print("# [1] 필터 입력")
    print("#----------------------------------------")
    filter_a = input_grid(3, "필터 A")
    print()
    filter_b = input_grid(3, "필터 B")

    # [2] 패턴 입력
    print()
    print("#----------------------------------------")
    print("# [2] 패턴 입력")
    print("#----------------------------------------")
    pattern = input_grid(3, "패턴")

    # MAC 연산 수행
    score_a = mac_operation(filter_a, pattern)
    score_b = mac_operation(filter_b, pattern)

    # 판정
    verdict = compare_scores_ab(score_a, score_b)

    # [3] MAC 결과 출력
    print()
    if verdict == "UNDECIDED":
        # 판정 불가: 점수를 16자리 소수점으로 표시, 연산 시간 생략
        print("#----------------------------------------")
        print("# [3] MAC 결과 (판정 불가)")
        print("#----------------------------------------")
        print(f"A 점수: {score_a:.16f}")
        print(f"B 점수: {score_b:.16f}")
        print("판정: 판정 불가 (|A-B| < 1e-9)")
    else:
        # 정상 판정: 시간 측정 포함
        # 두 필터 MAC 연산을 한 세트로 묶어 10회 반복 평균 측정
        repeat = 10
        start = time.perf_counter()
        for _ in range(repeat):
            mac_operation(filter_a, pattern)
            mac_operation(filter_b, pattern)
        end = time.perf_counter()
        avg_time_ms = (end - start) / repeat * 1000

        print("#----------------------------------------")
        print("# [3] MAC 결과")
        print("#----------------------------------------")
        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        print(f"연산 시간(평균/{repeat}회): {avg_time_ms:.3f} ms")
        print(f"판정: {verdict}")


if __name__ == "__main__":
    choice = show_menu()
    if choice == "1":
        run_mode_1()
    elif choice == "2":
        print("모드 2는 아직 구현되지 않았습니다.")
