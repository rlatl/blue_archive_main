# Blue Archive PC Main Screen Automation Test

이 저장소는 **블루 아카이브 PC판 Steam 버전**의 **메인 화면 UI 요소를 자동 검증**하는 테스트 스크립트를 포함합니다.  
**PyAutoGUI**와 **Python 표준 라이브러리** 및 **OpenCV** 기반으로 작성되었습니다.

테스트 스크립트는 각 UI 버튼을 찾아 클릭하고, 정상 작동 여부를 기록합니다.

---

## 📌 주요 기능

- 메인화면 내 12개 UI 요소 자동 클릭 테스트
- 로그 및 결과 파일 자동 저장
- 구글 시트 연동 (`upload_main.py`)
- 커맨드라인 인자 지원 (`--start`)
- 예기치 못한 화면으로 이동하거나 테스트 실패 시 방어 로직 및 복구 로직 구현

---

## 🖥️ 테스트 대상 UI 목록

| 순번 | 기능 이름         | CLI 인자 예시      |
|------|------------------|--------------------|
| 1    | 공지사항          | `--start 1`        |
| 2    | 모모톡            | `--start 2`        |
| 3    | 미션              | `--start 3`        |
| 4    | 청휘석 구입       | `--start 4`        |
| 5    | 카페              | `--start 5`        |
| 6    | 스케쥴            | `--start 6`        |
| 7    | 학생              | `--start 7`        |
| 8    | 편성              | `--start 8`        |
| 9    | 소셜              | `--start 9`        |
| 10   | 제작              | `--start 10`       |
| 11   | 상점              | `--start 11`       |
| 12   | 모집              | `--start 12`       |

---

## 📂 디렉토리 구조 예시

```
blue_archive_main/
├── main.py                 # 테스트 실행 메인 스크립트
├── config.toml            # 테스트 설정 파일
├── test_cases.json        # 테스트 항목 정의 파일
├── test_log.txt           # 실행 로그
├── test_results.txt       # 테스트 결과 요약
├── images/                # 버튼 이미지 리소스
│   ├── notice_button.png
│   ├── momo_button.png
│   ├── ...
```

## 🚀 실행 방법

```bash
# 테스트 전체 실행
python main.py

# 특정 테스트부터 실행
python main.py --start 5  # 카페부터 실행

# 실행 시 필요 사전 작업
images 폴더에 다음 이미지들 준비 필요

버튼 이미지: 메인 화면에 나타난 아이콘을 탐색하고 클릭함
bluepy_button.png
cafe_button.png
crafting_button.png
formation_button.png
lesson_button.png
mission_button.png
momo_button.png
notice_button.png
recruit_button.png
shop_button.png
social_button.png
students_button.png
students_special_button.png : 예외적으로 이 버튼은 '학생' 항목에 진입해 special 버튼을 누를때 필요

타겟 이미지 : 버튼을 통해 진입한 항목에 잘 진입했는지 확인용
bluepy_target.png
cafe_target.png
crafting_target.png
formation_target.png
lesson_target.png
mission_target.png
momo_target.png
notice_target.png
recruit_target.png
shop_target.png
social_target.png
students_target.png
students_target1.png
students_target2.png
students_special_target.png

닫기 이미지 : 각 항목에서 메인 화면으로 돌아갈때 클릭하는 이미지
bluepy_close.png
cafe_close.png
crafting_close.png
formation_close.png
lesson_close.png
mission_close.png
momo_close.png
notice_close.png
recruit_close.png
shop_close.png
social_close.png
students_close.png

기타 특수 기능 이미지 
main_event.png : 복구 로직 가동 이후 메인 화면으로 잘 복귀했나 확인용 ('이벤트 일람' 아이콘 사용)
notice1.png : 메인 화면에서 '공지' 진입 후 특정 세부 공지를 클릭하기 위한 이미지
special_activate.png : '학생' 항목에 진입했을때 현재 학생 목록이 스페셜인지 판별위한 이미지
striker.png : '학생' 항목에서 striker 버튼을 탐색하고 클릭하기 위한 이미지

```

---

## 📄 출력 파일

- `test_log.txt` – 테스트 로그 (실행 시점, 클릭 성공 여부 등)
- `test_results.txt` – 테스트 결과 (PASS / FAIL)

---

## ☁️ 구글 시트 연동

구글 클라우드 계정이 있다면, `upload_main.py`를 실행해 `test_results.txt`의 결과를 Google Sheets로 업로드할 수 있습니다.

---

## 🧰 사용 기술

- Python 3.x
- [PyAutoGUI](https://pypi.org/project/pyautogui/)
- OpenCV
- Google API (선택적, `upload_main.py`에서 사용)

```bash
pip install -r requirements.txt
```

---

## 📹 시연 영상 및 테스트 결과

## 👉 시연 영상 보기

- [블루아카이브 메인 화면 자동화 테스트](https://youtu.be/LAH9yk3UA8k)  
- [예외 상황 복구 및 스팀 클라이언트 렉 지속 테스트](https://youtu.be/0PilaoCcWsU)  
- [구글 시트에 테스트 결과 자동 입력](https://youtu.be/vN7u8v_onKI)

👉 [테스트 설계 및 결과 보기 (Google Sheet)](https://docs.google.com/spreadsheets/d/1RJwQvNWn9rVNjy3hYpxLwXlS4RYEvjnUWjgHTlPDYW8/edit?usp=sharing)

---

## 📁 기타

- 본 저장소는 자동화 포트폴리오 제출용으로 제작되었습니다.
