import pyautogui
import cv2
import mss
import numpy as np
import os
import time
import json
from datetime import datetime

# 경로 설정
current_path = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(current_path, "images")
result_file_path = os.path.join(current_path, "test_results.txt")
log_file_path = os.path.join(current_path, "test_log.txt")
test_case_file = os.path.join(current_path, "test_cases.json")

# 로그 기록 함수
def write_log(message):
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")

# 테스트 결과 기록 함수
def write_result(test_case, result):
    with open(result_file_path, "a", encoding="utf-8") as f:
        f.write(f"{test_case}: {result}\n")

# 이미지 검색 함수
def image_exists(template_path, threshold=0.9):
    try:
        with mss.mss() as sct:
            screen = sct.grab(sct.monitors[1])
            screen_np = np.array(screen)
            screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGRA2GRAY)
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template is None:
                write_log(f"Template not found: {template_path}")
                return False

            result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            return max_val >= threshold
    except Exception as e:
        write_log(f"image_exists error: {e}")
        return False

# 이미지 클릭 함수
def find_and_click(template_path, threshold=0.9):
    try:
        with mss.mss() as sct:
            screen = sct.grab(sct.monitors[1])
            screen_np = np.array(screen)
            screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGRA2GRAY)
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template is None:
                write_log(f"Template not found: {template_path}")
                return False

            result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                h, w = template.shape
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                write_log(f"Clicked image: {template_path}")
                return True
            else:
                write_log(f"Image not found (low confidence): {template_path} | confidence: {max_val}")
                return False
    except Exception as e:
        write_log(f"find_and_click error: {e}")
        return False

# 테스트 실행 함수
def run_tests():
    # 느린 케이스 목록
    slow_cases = ["cafe"]

    with open(test_case_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    for case in test_cases:
        button_img = os.path.join(image_dir, f"{case}.png")
        target_img = os.path.join(image_dir, f"{case}_target.png")
        close_img = os.path.join(image_dir, f"{case}_close.png")

        print(f"Testing: {case}")
        write_log(f"--- Start test: {case} ---")

        if find_and_click(button_img):
            wait_time = 5 if case in slow_cases else 3
            time.sleep(wait_time)  # 로딩 대기

            if image_exists(target_img):
                write_result(case, "PASS")
                write_log(f"{case}: PASS")
            else:
                write_result(case, "FAIL (target not found)")
                write_log(f"{case}: FAIL (target not found)")

            time.sleep(2)

            # 닫기 버튼 시도
            if not find_and_click(close_img):
                write_log(f"{case}: close image not found")
            time.sleep(wait_time)

        else:
            write_result(case, "FAIL (button not found)")
            write_log(f"{case}: FAIL (button not found)")

    print("테스트 완료.")
    write_log("=== All tests completed ===")

# 메인 함수
if __name__ == "__main__":
    run_tests()

