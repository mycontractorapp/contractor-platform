from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# 🔐 ใส่ชื่อไฟล์ JSON ที่คุณมี
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("contractorplatform-894f2456a582.json", scope)
client = gspread.authorize(creds)

# ✅ ชื่อ Google Sheet ต้องตรงกับชื่อจริง
sheet = client.open("contractors_register").sheet1

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    province = request.form['province']
    job_type = request.form['job_type']
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([name, phone, province, job_type, now])
    return "✅ บันทึกข้อมูลเรียบร้อยแล้ว!"

if __name__ == '__main__':
    app.run(debug=True)
