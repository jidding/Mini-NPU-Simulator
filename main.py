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

def input_matrix_3x3(matrix_name):
    """
    3x3 행렬을 한 줄씩(공백 구분) 입력받아 2차원 리스트로 반환합니다.
    행/열 개수 불일치 및 숫자 변환 오류 시 재입력을 유도합니다.
    """
    print(f"\n{matrix_name} (3줄 입력, 공백 구분)")
    matrix = []
    
    for row_idx in range(1, 4):
        while True:
            raw_input = input(f"{row_idx}번째 줄: ").strip()
            parts = raw_input.split()
            
            # 1) 열 개수 검증 (빈 입력 포함)
            if len(parts) != 3:
                print("⚠️ 입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
                continue
                
            # 2) 숫자 파싱 검증
            try:
                row = [float(x) for x in parts]
                matrix.append(row)
                break
            except ValueError:
                print("⚠️ 입력 형식 오류: 숫자만 입력해야 합니다. 다시 입력하세요.")
                
    return matrix

def run_mode_1():
    """
    모드 1: 사용자 입력(3x3) 전체 실행 흐름
    """
    print("\n#----------------------------------------")
    print("# [1] 필터 입력")
    print("#----------------------------------------")
    filter_a = input_matrix_3x3("필터 A")
    filter_b = input_matrix_3x3("필터 B")
    
    print("\n#----------------------------------------")
    print("# [2] 패턴 입력")
    print("#----------------------------------------")
    pattern = input_matrix_3x3("패턴")
    
    # MAC 연산 수행
    score_a = mac_operation(pattern, filter_a)
    score_b = mac_operation(pattern, filter_b)
    
    # 연산 시간 측정 (10회 평균, ms)
    avg_time_ms = measure_mac_time(pattern, filter_a, iterations=10)
    
    # 결과 판정
    result = judge_scores(score_a, score_b, label_a="A", label_b="B", tie_label="판정 불가 (|A-B| < 1e-9)")
    
    print("\n#----------------------------------------")
    print("# [3] MAC 결과")
    print("#----------------------------------------")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {avg_time_ms:.4f} ms")
    print(f"판정: {result}")

def main():
    while True:
        print("\n=== Mini NPU Simulator ===")
        print("[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("0. 종료")
        
        choice = input("선택: ").strip()
        
        if choice == "1":
            run_mode_1()
        elif choice == "2":
            print("\n🚧 data.json 분석 기능은 다음 스텝(Step 4)에서 구현합니다.")
        elif choice == "0":
            print("시뮬레이터를 종료합니다.")
            break
        else:
            print("⚠️ 잘못된 선택입니다. 1, 2, 0 중 하나를 입력하세요.")

if __name__ == "__main__":
    main()