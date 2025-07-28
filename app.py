from flask import Flask, request, render_template
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# อ่านค่า JSON จาก Environment Variable
SERVICE_ACCOUNT_JSON = os.getenv("SERVICE_ACCOUNT_JSON")

# แปลง JSON String เป็น dict
service_account_info = json.loads(SERVICE_ACCOUNT_JSON)

# ตั้งค่า scope และ credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# เปิด Google Sheet ตามชื่อ
sheet = client.open("ContractorPlatform").sheet1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        province = request.form['province']
        work_type = request.form['work_type']
        
        # เพิ่มข้อมูลลงในแถวใหม่
        sheet.append_row([name, phone, province, work_type])
        return 'ส่งข้อมูลเรียบร้อยแล้ว! ✅'
    
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
