# main.py — Mini NPU Simulator

from typing import List  # Python 3.8 호환성 지원을 위해 사용 (3.9+에서는 내장 list로 대체 가능)


def create_grid(n: int, default_value: float = 0.0) -> List[List[float]]:
    """n×n 크기의 2D 배열을 생성하여 반환한다."""
    return [[default_value] * n for _ in range(n)]


def get_value(grid: List[List[float]], row: int, col: int) -> float:
    """2D 배열의 (row, col) 위치 값을 읽는다."""
    return grid[row][col]


def set_value(grid: List[List[float]], row: int, col: int, value: float) -> None:
    """2D 배열의 (row, col) 위치에 값을 저장한다."""
    grid[row][col] = value


if __name__ == "__main__":
    pass  # Phase 2 이후 모드 선택 메뉴 연결 예정
