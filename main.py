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

# 이미지 존재 여부 확인 함수
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
    slow_cases = ["cafe"]
    with open(test_case_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    for case in test_cases:
        button_img = os.path.join(image_dir, f"{case}.png")
        close_img = os.path.join(image_dir, f"{case}_close.png")

        print(f"Testing: {case}")
        write_log(f"--- Start test: {case} ---")

        if not find_and_click(button_img):
            write_result(case, "FAIL (button not found)")
            write_log(f"{case}: FAIL (button not found)")
            continue

        wait_time = 5 if case in slow_cases else 3
        time.sleep(wait_time)

        if case == "students":
            # 학생 항목 특수 처리
            target1 = os.path.join(image_dir, "students_target1.png")
            target2 = os.path.join(image_dir, "students_target2.png")
            special_btn = os.path.join(image_dir, "students_special_button.png")
            target3 = os.path.join(image_dir, "students_special_target.png")

            ok1 = image_exists(target1)
            ok2 = image_exists(target2)
            if find_and_click(special_btn):
                time.sleep(2)
                ok3 = image_exists(target3)
            else:
                ok3 = False

            if ok1 and ok2 and ok3:
                write_result(case, "PASS")
                write_log(f"{case}: PASS (3 target checks passed)")
            else:
                write_result(case, "FAIL (target check failed)")
                write_log(f"{case}: FAIL (one or more target checks failed)")

        elif case == "notice":
            # 공지사항 항목: notice → notice1 클릭 → target 스크롤 탐색
            notice1 = os.path.join(image_dir, "notice1.png")
            target_img = os.path.join(image_dir, "notice_target.png")

            time.sleep(4)

            if not find_and_click(notice1):
                write_result(case, "FAIL (notice1 not found)")
                write_log(f"{case}: FAIL (notice1 not found)")
                continue

            time.sleep(3)

            found = False
            for _ in range(15):
                if image_exists(target_img):
                    found = True
                    break
                pyautogui.scroll(-1000)
                time.sleep(1)

            if found:
                write_result(case, "PASS")
                write_log(f"{case}: PASS (target found after scrolling)")
            else:
                write_result(case, "FAIL (target not found)")
                write_log(f"{case}: FAIL (target not found after scrolling)")

        else:
            # 기본 케이스
            target_img = os.path.join(image_dir, f"{case}_target.png")
            if image_exists(target_img):
                write_result(case, "PASS")
                write_log(f"{case}: PASS")
            else:
                write_result(case, "FAIL (target not found)")
                write_log(f"{case}: FAIL (target not found)")

        time.sleep(2)
        if not find_and_click(close_img):
            write_log(f"{case}: close image not found")
        time.sleep(wait_time)

    print("테스트 완료.")
    write_log("=== All tests completed ===")

# 메인 함수
if __name__ == "__main__":
    run_tests()
