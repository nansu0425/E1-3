# main.py — Mini NPU Simulator

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


if __name__ == "__main__":
    pass  # Phase 3 이후 모드 선택 메뉴 연결 예정
