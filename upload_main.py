import gspread
from oauth2client.service_account import ServiceAccountCredentials

def upload_results():
    # 인증
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # 문서 및 워크시트 열기
    spreadsheet = client.open("블루아카이브 자동화 테스트 QA")
    sheet = spreadsheet.worksheet("블루아카이브 자동화 - pc 메인 화면 QA")

    # 결과 읽기
    with open("test_results.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # D4부터 업데이트
    start_row = 4
    for i, line in enumerate(lines):
        if "PASS" in line:
            value = "PASS"
        elif "FAIL" in line:
            value = "FAIL"
        else:
            value = "N/A"

        cell = f"D{start_row + i}"
        sheet.update_acell(cell, value)
        print(f"{cell}에 '{value}' 입력 완료")

if __name__ == "__main__":
    upload_results()
