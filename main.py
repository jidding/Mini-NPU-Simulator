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

def normalize_label(raw_label):
    """
    다양한 입력 라벨('+', 'cross', 'x' 등)을 내부 표준 라벨('Cross', 'X')로 정규화합니다.
    """
    if not isinstance(raw_label, str):
        return "UNKNOWN"
    cleaned = raw_label.strip().lower()
    if cleaned in ("+", "cross"):
        return "Cross"
    elif cleaned == "x":
        return "X"
    return raw_label

def is_valid_matrix(matrix, expected_size):
    """
    전달받은 2차원 리스트가 정확히 expected_size x expected_size 크기인지 검증합니다.
    """
    if not isinstance(matrix, list) or len(matrix) != expected_size:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != expected_size:
            return False
    return True

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

def print_performance_table(normalized_filters):
    """
    3x3, 5x5, 13x13, 25x25 크기의 MAC 평균 연산 시간(10회)과 연산 횟수(N^2) 표를 출력합니다.
    """
    print("\n#---------------------------------------")
    print("# [3] 성능 분석 (평균/10회)")
    print("#---------------------------------------")
    print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수'}")
    print("-" * 40)

    # 3x3 기본 테스트용 패턴/필터 준비
    sample_3x3 = [
        [0.0, 1.0, 0.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 0.0]
    ]
    time_3x3 = measure_mac_time(sample_3x3, sample_3x3, iterations=10)
    print(f"{'3×3':<10} {time_3x3:<15.4f} {3 * 3}")

    # 5x5, 13x13, 25x25 측정 (data.json에서 로드된 Cross 필터 활용)
    for size in (5, 13, 25):
        size_key = f"size_{size}"
        if size_key in normalized_filters and "Cross" in normalized_filters[size_key]:
            mat = normalized_filters[size_key]["Cross"]
            avg_ms = measure_mac_time(mat, mat, iterations=10)
            print(f"{f'{size}×{size}':<10} {avg_ms:<15.4f} {size * size}")

def run_mode_2(filepath="data.json"):
    """
    모드 2: data.json 로드, 스키마/크기 검증, 일괄 MAC 판정, 성능 분석 및 결과 요약을 수행합니다.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ 오류: '{filepath}' 파일을 찾을 수 없습니다. 프로젝트 루트 경로를 확인하세요.")
        return
    except json.JSONDecodeError:
        print(f"⚠️ 오류: '{filepath}' 파일의 JSON 형식이 손상되었습니다.")
        return

    raw_filters = data.get("filters", {})
    raw_patterns = data.get("patterns", {})

    # 1. 필터 로드 및 라벨 정규화
    print("\n#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")
    normalized_filters = {}
    for size_key, filter_dict in raw_filters.items():
        normalized_filters[size_key] = {}
        for raw_label, matrix in filter_dict.items():
            std_label = normalize_label(raw_label)
            normalized_filters[size_key][std_label] = matrix
        loaded_labels = ", ".join(normalized_filters[size_key].keys())
        print(f"✓ {size_key:<7} 필터 로드 완료 ({loaded_labels})")

    # 2. 패턴 일괄 분석
    print("\n#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#---------------------------------------")
    total_tests = 0
    passed_tests = 0
    failed_cases = []

    for case_id, case_info in raw_patterns.items():
        total_tests += 1
        print(f"-- {case_id} ---")

        # 키 이름(예: size_5_1)에서 크기 N 추출
        try:
            n = int(case_id.split("_")[1])
        except (IndexError, ValueError):
            reason = "키 형식 오류로 크기 N을 추출할 수 없음"
            print(f"판정: ERROR | FAIL ({reason})")
            failed_cases.append((case_id, reason))
            continue

        size_key = f"size_{n}"
        input_matrix = case_info.get("input")
        expected_std = normalize_label(case_info.get("expected"))

        # 필터 존재 여부 및 크기 일치 검증
        if size_key not in normalized_filters:
            reason = f"해당 크기({size_key})의 기준 필터가 존재하지 않음"
            print(f"판정: ERROR | FAIL ({reason})")
            failed_cases.append((case_id, reason))
            continue

        cross_filter = normalized_filters[size_key].get("Cross")
        x_filter = normalized_filters[size_key].get("X")

        if not is_valid_matrix(input_matrix, n) or not is_valid_matrix(cross_filter, n) or not is_valid_matrix(x_filter, n):
            reason = f"배열 크기 불일치 (기대 크기: {n}×{n})"
            print(f"판정: ERROR | expected: {expected_std} | FAIL ({reason})")
            failed_cases.append((case_id, reason))
            continue

        # MAC 연산 및 판정
        score_cross = mac_operation(input_matrix, cross_filter)
        score_x = mac_operation(input_matrix, x_filter)
        judgment = judge_scores(score_cross, score_x, label_a="Cross", label_b="X", tie_label="UNDECIDED")

        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")

        if judgment == expected_std:
            passed_tests += 1
            print(f"판정: {judgment} | expected: {expected_std} | PASS")
        else:
            if judgment == "UNDECIDED":
                reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
            else:
                reason = f"판정 불일치 (판정: {judgment}, 기대값: {expected_std})"
            print(f"판정: {judgment} | expected: {expected_std} | FAIL ({reason})")
            failed_cases.append((case_id, reason))

    # 3. 크기별 성능 분석 표 출력
    print_performance_table(normalized_filters)

    # 4. 최종 결과 요약 리포트 출력
    print("\n#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {total_tests}개")
    print(f"통과: {passed_tests}개")
    print(f"실패: {len(failed_cases)}개")

    if failed_cases:
        print("\n실패 케이스:")
        for cid, msg in failed_cases:
            print(f"- {cid}: {msg}")

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
            run_mode_2()
        elif choice == "0":
            print("시뮬레이터를 종료합니다.")
            break
        else:
            print("⚠️ 잘못된 선택입니다. 1, 2, 0 중 하나를 입력하세요.")

if __name__ == "__main__":
    main()