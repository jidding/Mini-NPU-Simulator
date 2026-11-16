import json
import time

def mac_operation(pattern, filter_matrix):
    """
    n x n 크기의 pattern과 filter_matrix를 위치별로 곱하고 누적하여 합산(MAC)합니다.
    (외부 라이브러리 없이 순수 이중 반복문 사용)
    """
    n = len(pattern)
    total_score = 0.0
    
    for i in range(n):
        for j in range(n):
            total_score += pattern[i][j] * filter_matrix[i][j]
            
    return total_score

EPSILON = 1e-9  # 부동소수점 동점 판별 허용오차

def judge_scores(score_a, score_b, label_a="A", label_b="B", tie_label="판정 불가"):
    """
    두 필터의 점수를 허용오차(epsilon) 기준으로 비교하여 판정 결과를 반환합니다.
    """
    if abs(score_a - score_b) < EPSILON:
        return tie_label
    return label_a if score_a > score_b else label_b

def measure_mac_time(pattern, filter_matrix, iterations=10):
    """
    I/O 시간을 제외하고 순수 MAC 연산 함수 호출 구간만 iterations(기본 10회) 반복 측정하여
    평균 연산 시간(ms)을 반환합니다.
    """
    start_time = time.perf_counter()
    for _ in range(iterations):
        mac_operation(pattern, filter_matrix)
    end_time = time.perf_counter()
    
    avg_time_ms = ((end_time - start_time) / iterations) * 1000
    return avg_time_ms

# 간단한 동작 테스트 (3x3 십자가 예시)
if __name__ == "__main__":
    cross_filter = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]
    print("테스트 MAC 점수:", mac_operation(cross_filter, cross_filter))  # 5.0이 출력되어야 정상