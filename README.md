# K403 Dashboard — ทะเบียนครุภัณฑ์การแพทย์

Dashboard สำหรับแสดงและค้นหาข้อมูลครุภัณฑ์การแพทย์ K403 จำนวน 6,380 รายการ

## โครงสร้างไฟล์

```
database_dashboard/
├── index.html        ← Dashboard หลัก
├── data/
│   └── k403.json    ← ฐานข้อมูล (1.89 MB)
└── README.md
```

## วิธี Push ขึ้น GitHub

### 1. เปิด Terminal (Command Prompt หรือ Git Bash) แล้วรันคำสั่งต่อไปนี้

```bash
# เข้าโฟลเดอร์
cd "D:\Cowork\K403\database_dashboard"

# ถ้ายังไม่เคย init git
git init
git remote add origin https://github.com/YOUR_USERNAME/database_dashboard.git

# ถ้ามี repo อยู่แล้ว ให้ clone ก่อน แล้ว copy ไฟล์เข้าไป
# git clone https://github.com/YOUR_USERNAME/database_dashboard.git

# Add และ commit
git add .
git commit -m "Add K403 Dashboard v1"
git push -u origin main
```

> แทน `YOUR_USERNAME` ด้วย GitHub username ของคุณ

### 2. เปิด GitHub Pages

1. เข้า repo บน GitHub
2. ไปที่ **Settings → Pages**
3. Source: เลือก **Deploy from a branch**
4. Branch: `main` / folder: `/ (root)`
5. กด **Save**
6. รอ ~1 นาที แล้วเข้าได้ที่ `https://YOUR_USERNAME.github.io/database_dashboard/`

## ฟีเจอร์ Dashboard

| ฟีเจอร์ | รายละเอียด |
|---|---|
| 📊 KPI | รวมรายการ, ใช้งานอยู่, จำหน่ายแล้ว, ประเภท, หน่วยงาน, ยี่ห้อ |
| 📦 กราฟประเภท | Top 15 ประเภทเครื่องมือ |
| 📅 กราฟปี | จำนวนตามปีที่ได้รับ (พ.ศ.) |
| 🏷️ กราฟยี่ห้อ | Top 15 ยี่ห้อ |
| ⚙️ กราฟสถานะ | Donut chart ใช้งาน vs จำหน่าย |
| 🔍 ค้นหา | ค้นหาชื่อ ยี่ห้อ ID Number |
| 🎛️ กรอง | ประเภท หน่วยงาน ปี พ.ศ. (จาก-ถึง) ยี่ห้อ สถานะ |
| ↕️ เรียง | ID, ปีเก่า→ใหม่, ปีใหม่→เก่า, ราคา, ยี่ห้อ, หน่วยงาน |
| 🏥 สรุปหน่วยงาน | จำนวนรายการต่อหน่วยงาน + bar chart |

## อัปเดตข้อมูล

เมื่อต้องการอัปเดต แปลง Excel ใหม่เป็น `k403.json` แล้ว push ขึ้น GitHub อีกครั้ง

```bash
git add data/k403.json
git commit -m "Update K403 data YYYY-MM-DD"
git push
```
