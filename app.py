from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# ใช้ Scope สำหรับ Google Sheets และ Drive API
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# โหลด credentials จาก Environment Variable
google_creds_json = os.environ.get('GOOGLE_SHEET_CREDENTIALS')
creds_dict = json.loads(google_creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# สร้าง client และเปิด spreadsheet
client = gspread.authorize(creds)
sheet = client.open("ContractorPlatform").sheet1  # ชื่อ Google Sheet ของคุณ

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        province = request.form['province']
        job_type = request.form['job_type']
        sheet.append_row([name, phone, province, job_type])
        return "ส่งข้อมูลเรียบร้อยแล้ว ✅"
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
