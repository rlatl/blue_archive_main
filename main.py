import pyautogui
import cv2
import mss
import numpy as np
import os
import time
import json
from datetime import datetime
import toml
import argparse

#--start 1  : notice  
#--start 2  : momo  
#--start 3  : mission  
#--start 4  : bluepy  
#--start 5  : cafe  
#--start 6  : lesson  
#--start 7  : students  
#--start 8  : formation  
#--start 9  : social  
#--start 10 : crafting  
#--start 11 : shop  
#--start 12 : recruit  


# 설정 로드
config = toml.load("config.toml")
REPEAT = config["settings"].get("repeat", 3)
SLOW_DELAY = config["settings"].get("slow_case_delay", 5)
NORMAL_DELAY = config["settings"].get("normal_case_delay", 3)

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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(result_file_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {test_case}: {result}\n")

# 이미지 확인
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

# 이미지 클릭
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
                write_log(f"Image not found: {template_path} | confidence: {max_val}")
                return False
    except Exception as e:
        write_log(f"find_and_click error: {e}")
        return False

# 복구 함수
def attempt_recovery():
    back_button = (15, 48)
    main_img = os.path.join(image_dir, "main_campaign.png")
    notice_close_img = os.path.join(image_dir, "notice_close.png")

    attempt = 0
    while not image_exists(main_img):
        if image_exists(notice_close_img):
            find_and_click(notice_close_img)
            write_log(f"Recovery attempt {attempt + 1}: clicked notice_close")
        else:
            pyautogui.click(back_button)
            write_log(f"Recovery attempt {attempt + 1}: clicked back button")
        time.sleep(3)
        attempt += 1
    write_log("Recovery success: main screen detected")

# 단계별 테스트 실행
def run_step(case):
    button_img = os.path.join(image_dir, f"{case}_button.png")
    close_img = os.path.join(image_dir, f"{case}_close.png")

    print(f"Testing: {case}")
    write_log(f"--- Start test: {case} ---")

    if not find_and_click(button_img):
        write_log(f"{case}: button not found, initiating recovery...")
        attempt_recovery()
        if not find_and_click(button_img):
            write_result(case, "FAIL (button not found after recovery)")
            return

    delay = SLOW_DELAY if case == "cafe" else NORMAL_DELAY
    time.sleep(delay)

    if case == "students":
        special_activate_img = os.path.join(image_dir, "special_activate.png")
        striker_img = os.path.join(image_dir, "striker.png")

        if image_exists(special_activate_img):
            write_log("special_activate.png detected")
            if find_and_click(striker_img):
                write_log("Clicked striker.png")
                time.sleep(2)

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
        else:
            write_result(case, "FAIL (target check failed)")

    elif case == "notice":
        notice1 = os.path.join(image_dir, "notice1.png")
        target_img = os.path.join(image_dir, "notice_target.png")

        time.sleep(4)
        if not find_and_click(notice1):
            write_result(case, "FAIL (notice1 not found)")
            attempt_recovery()
            return

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
        else:
            write_result(case, "FAIL (target not found after scrolling)")

    else:
        target_img = os.path.join(image_dir, f"{case}_target.png")
        if image_exists(target_img):
            write_result(case, "PASS")
        else:
            write_result(case, "FAIL (target not found)")
            attempt_recovery()

    time.sleep(2)
    if not find_and_click(close_img):
        write_log(f"{case}: close image not found, initiating recovery...")
        attempt_recovery()

    time.sleep(delay)

# 전체 테스트 루프
def run_tests_from_step(start_step=0):
    with open(test_case_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    for run in range(REPEAT):
        write_log(f"==== Run {run + 1} / {REPEAT} ====")
        for i, case in enumerate(test_cases):
            if i >= start_step:
                run_step(case)
        write_log(f"==== Run {run + 1} completed ====")
    write_log("=== All tests completed ===")
    print("테스트 완료.")

# main
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1, help="테스트 시작 단계 index (1부터 시작)")
    args = parser.parse_args()
    start_index = max(0, args.start - 1)
    run_tests_from_step(start_index)
