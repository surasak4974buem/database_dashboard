#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, urllib.request

# ── Download Thai-capable font (Sarabun from Google Fonts) ──────────────────
FONT_DIR = "/tmp/fonts"
os.makedirs(FONT_DIR, exist_ok=True)

font_urls = {
    "Sarabun":       "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Regular.ttf",
    "Sarabun-Bold":  "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Bold.ttf",
}

for name, url in font_urls.items():
    path = f"{FONT_DIR}/{name}.ttf"
    if not os.path.exists(path):
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, path)
    pdfmetrics.registerFont(TTFont(name, path))

# ── Document setup ───────────────────────────────────────────────────────────
OUTPUT = "/home/user/database_dashboard/คู่มือตรวจเช็คงานซ่อมเครื่องมือแพทย์.pdf"
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=20*mm, bottomMargin=20*mm,
)

W, H = A4

# ── Styles ───────────────────────────────────────────────────────────────────
DARK_BLUE  = colors.HexColor("#003366")
MED_BLUE   = colors.HexColor("#005A9C")
LIGHT_BLUE = colors.HexColor("#D6E4F0")
RED        = colors.HexColor("#C0392B")
ORANGE     = colors.HexColor("#E67E22")
GREEN      = colors.HexColor("#1E8449")
GRAY       = colors.HexColor("#7F8C8D")
LGRAY      = colors.HexColor("#F2F3F4")
WHITE      = colors.white

def style(name="Sarabun", size=10, color=colors.black, bold=False,
          align=TA_LEFT, leading=None, space_before=0, space_after=2):
    font = "Sarabun-Bold" if bold else "Sarabun"
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        textColor=color,
        alignment=align,
        leading=leading or size * 1.4,
        spaceBefore=space_before * mm,
        spaceAfter=space_after * mm,
    )

s_title   = style(size=18, color=WHITE, bold=True, align=TA_CENTER, leading=24)
s_sub     = style(size=12, color=WHITE, align=TA_CENTER, leading=16)
s_h1      = style(size=13, color=DARK_BLUE, bold=True, space_before=4, space_after=2)
s_h2      = style(size=11, color=MED_BLUE, bold=True, space_before=3, space_after=1)
s_body    = style(size=10, leading=15)
s_small   = style(size=9, color=GRAY)
s_center  = style(size=10, align=TA_CENTER)
s_warn    = style(size=9, color=RED)
s_bold    = style(size=10, bold=True)
s_th      = style(size=9, color=WHITE, bold=True, align=TA_CENTER)
s_td      = style(size=9, align=TA_CENTER)
s_td_l    = style(size=9, align=TA_LEFT)

story = []

# ══════════════════════════════════════════════════════════════════════════════
# HEADER BANNER
# ══════════════════════════════════════════════════════════════════════════════
banner_data = [[
    Paragraph("คู่มือปฏิบัติงาน", s_title),
    ""
],[
    Paragraph("การตรวจเช็คงานซ่อมเครื่องมือแพทย์ก่อนเริ่มงานประจำวัน", s_sub),
    ""
]]
banner = Table(banner_data, colWidths=[W - 40*mm])
banner.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), DARK_BLUE),
    ("BOX",          (0,0), (-1,-1), 1, MED_BLUE),
    ("TOPPADDING",   (0,0), (-1,-1), 6),
    ("BOTTOMPADDING",(0,0), (-1,-1), 6),
    ("SPAN",         (0,0), (-1,0)),
    ("SPAN",         (0,1), (-1,1)),
]))
story.append(banner)
story.append(Spacer(1, 4*mm))

# ── Meta info table ──────────────────────────────────────────────────────────
meta = [
    ["ฉบับที่",          "001",   "วันที่บังคับใช้", "มิถุนายน 2569"],
    ["แผนก",            "วิศวกรรมการแพทย์ / ซ่อมบำรุงเครื่องมือแพทย์", "เวลาปฏิบัติงาน", "08:30 – 16:30 น."],
    ["วันทำการ",         "จันทร์ – ศุกร์ (วันราชการ)", "ผู้รับผิดชอบ", "ช่างเครื่องมือแพทย์ / วิศวกรชีวการแพทย์"],
]
mt = Table(meta, colWidths=[32*mm, 65*mm, 38*mm, 35*mm])
mt.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (0,-1), LIGHT_BLUE),
    ("BACKGROUND",   (2,0), (2,-1), LIGHT_BLUE),
    ("FONTNAME",     (0,0), (0,-1), "Sarabun-Bold"),
    ("FONTNAME",     (2,0), (2,-1), "Sarabun-Bold"),
    ("FONTNAME",     (1,0), (1,-1), "Sarabun"),
    ("FONTNAME",     (3,0), (3,-1), "Sarabun"),
    ("FONTSIZE",     (0,0), (-1,-1), 9),
    ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
    ("TOPPADDING",   (0,0), (-1,-1), 4),
    ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ("LEFTPADDING",  (0,0), (-1,-1), 4),
]))
story.append(mt)
story.append(Spacer(1, 5*mm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — วัตถุประสงค์
# ══════════════════════════════════════════════════════════════════════════════
story.append(HRFlowable(width="100%", thickness=2, color=DARK_BLUE))
story.append(Paragraph("1. วัตถุประสงค์", s_h1))
story.append(Paragraph(
    "เพื่อคัดกรองและจัดลำดับความสำคัญของงานซ่อมเครื่องมือแพทย์ก่อนเริ่มปฏิบัติงานทุกวัน "
    "ให้งานที่เร่งด่วนและส่งผลต่อความปลอดภัยของผู้ป่วยได้รับการแก้ไขก่อนเป็นลำดับแรก", s_body))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — เกณฑ์ระดับความเร่งด่วน
# ══════════════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 3*mm))
story.append(HRFlowable(width="100%", thickness=2, color=DARK_BLUE))
story.append(Paragraph("2. เกณฑ์จำแนกระดับความเร่งด่วน", s_h1))

urg_header = [
    [Paragraph("ระดับ", s_th), Paragraph("รหัส", s_th),
     Paragraph("ความหมาย", s_th), Paragraph("ระยะเวลาตอบสนอง", s_th)]
]
urg_rows = [
    [Paragraph("วิกฤต", style(size=9, color=WHITE, bold=True, align=TA_CENTER)),
     Paragraph("D1", style(size=9, color=WHITE, bold=True, align=TA_CENTER)),
     Paragraph("เครื่องมือเกี่ยวข้องกับชีวิตผู้ป่วยโดยตรง\nหรือหน่วย ICU / ER / OR", s_td_l),
     Paragraph("ทันที (ภายใน 1 ชั่วโมง)", style(size=9, color=WHITE, bold=True, align=TA_CENTER))],
    [Paragraph("เร่งด่วน", s_td),
     Paragraph("D2", s_td),
     Paragraph("กระทบการรักษา/วินิจฉัย แต่มีเครื่องสำรอง", s_td_l),
     Paragraph("ภายใน 4 ชั่วโมง", s_td)],
    [Paragraph("ปกติ", s_td),
     Paragraph("D3", s_td),
     Paragraph("ไม่กระทบการรักษาในทันที", s_td_l),
     Paragraph("ภายใน 24–48 ชั่วโมง", s_td)],
    [Paragraph("แผน PM", s_td),
     Paragraph("PM", s_td),
     Paragraph("งานตามกำหนดการ Preventive Maintenance", s_td_l),
     Paragraph("ตามแผนที่กำหนด", s_td)],
]
urg_data = urg_header + urg_rows
urg_t = Table(urg_data, colWidths=[22*mm, 14*mm, 85*mm, 49*mm])
urg_t.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), DARK_BLUE),
    ("BACKGROUND",   (0,1), (-1,1), RED),
    ("BACKGROUND",   (0,2), (-1,2), colors.HexColor("#FEF9E7")),
    ("BACKGROUND",   (0,3), (-1,3), colors.HexColor("#EAFAF1")),
    ("BACKGROUND",   (0,4), (-1,4), LGRAY),
    ("FONTNAME",     (0,1), (-1,1), "Sarabun-Bold"),
    ("TEXTCOLOR",    (0,1), (-1,1), WHITE),
    ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
    ("TOPPADDING",   (0,0), (-1,-1), 4),
    ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ("LEFTPADDING",  (0,0), (-1,-1), 4),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
]))
story.append(urg_t)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — ขั้นตอน Morning Round
# ══════════════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 3*mm))
story.append(HRFlowable(width="100%", thickness=2, color=DARK_BLUE))
story.append(Paragraph("3. ขั้นตอนการตรวจเช็คตอนเช้า — Morning Round", s_h1))
story.append(Paragraph("เวลาที่แนะนำ: 08:30 – 09:00 น. (ก่อนเริ่มงานซ่อม)", s_small))
story.append(Spacer(1, 2*mm))

steps = [
    ("ขั้นที่ 1", MED_BLUE,
     "ตรวจสอบใบแจ้งซ่อมค้างจากวันก่อน",
     ["เปิดระบบแจ้งซ่อม (CMMS / ระบบโรงพยาบาล)",
      "ตรวจสอบงานค้างที่ยังไม่เสร็จ และงานที่รอชิ้นส่วนอะไหล่",
      "บันทึกสถานะล่าสุดของงานค้างทุกรายการ"]),
    ("ขั้นที่ 2", MED_BLUE,
     "รับและคัดกรองใบแจ้งซ่อมใหม่",
     ["ตรวจสอบระบบแจ้งซ่อมออนไลน์ / สมุดรับแจ้งซ่อม / LINE / E-mail",
      "ถามผู้แจ้งซ่อม: เครื่องเกี่ยวข้องกับผู้ป่วยโดยตรงหรือไม่?",
      "ถามผู้แจ้งซ่อม: มีผู้ป่วยรอใช้งานอยู่ขณะนี้หรือไม่?",
      "ถามผู้แจ้งซ่อม: มีเครื่องสำรองทดแทนได้หรือไม่?",
      "ถามผู้แจ้งซ่อม: อยู่ใน ICU / ER / OR / NICU หรือไม่?"]),
    ("ขั้นที่ 3", MED_BLUE,
     "จัดทำ Daily Work List จัดเรียงลำดับ D1 → D2 → D3 → PM",
     ["จัดลำดับงานตามระดับความเร่งด่วน",
      "ระบุชื่อเครื่องมือ หน่วยงาน และชื่อผู้แจ้งซ่อม"]),
    ("ขั้นที่ 4", MED_BLUE,
     "มอบหมายงานและเตรียมทรัพยากร",
     ["มอบหมายช่างตามความเชี่ยวชาญและประเภทเครื่องมือ",
      "ตรวจสอบความพร้อมของเครื่องมือช่าง / อะไหล่",
      "แจ้งหน่วยงานผู้ใช้ทราบกำหนดการเข้าซ่อม"]),
    ("ขั้นที่ 5", MED_BLUE,
     "สรุปและรายงาน",
     ["บันทึกรายการงานประจำวันลงในระบบหรือแบบฟอร์ม ME-F-01",
      "รายงานงาน D1 ต่อหัวหน้าหน่วยทันที",
      "อัปเดตสถานะงานในระบบทุก 2 ชั่วโมง"]),
]

for step_no, color, title, bullets in steps:
    row = [[
        Paragraph(step_no, style(size=9, color=WHITE, bold=True, align=TA_CENTER)),
        Paragraph(title, style(size=10, color=DARK_BLUE, bold=True)),
    ]]
    t = Table(row, colWidths=[18*mm, W - 40*mm - 18*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (0,0), color),
        ("BACKGROUND",   (1,0), (1,0), LIGHT_BLUE),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LEFTPADDING",  (0,0), (-1,-1), 4),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("BOX",          (0,0), (-1,-1), 0.5, MED_BLUE),
    ]))
    story.append(t)
    for b in bullets:
        story.append(Paragraph(f"   ✓  {b}", s_body))
    story.append(Spacer(1, 1*mm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — เครื่องมือกลุ่มเสี่ยงสูง
# ══════════════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 2*mm))
story.append(HRFlowable(width="100%", thickness=2, color=DARK_BLUE))
story.append(Paragraph("4. เครื่องมือแพทย์กลุ่มเสี่ยงสูง (แก้ไขก่อนเสมอ)", s_h1))

hi_risk = [
    ["เครื่องช่วยหายใจ (Ventilator)", "เครื่องกระตุกหัวใจ (Defibrillator / AED)"],
    ["เครื่องดมยาสลบ (Anesthesia Machine)", "เครื่องให้ยาอัตโนมัติ (Infusion / Syringe Pump)"],
    ["เครื่องฟอกไต (Dialysis Machine)", "เครื่องตรวจติดตามผู้ป่วย (Patient Monitor)"],
    ["เครื่อง X-ray / CT Scan (กรณีด่วน)", "เครื่องให้ออกซิเจน (O2 Concentrator)"],
]
hr_data = [[Paragraph(a, s_td_l), Paragraph(b, s_td_l)] for a, b in hi_risk]
hr_t = Table(hr_data, colWidths=[(W - 40*mm) / 2, (W - 40*mm) / 2])
hr_t.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#FDEDEC")),
    ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#F1948A")),
    ("TOPPADDING",   (0,0), (-1,-1), 4),
    ("BOTTOMPADDING",(0,0), (-1,-1), 4),
]))
story.append(hr_t)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Escalation
# ══════════════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 3*mm))
story.append(HRFlowable(width="100%", thickness=2, color=DARK_BLUE))
story.append(Paragraph("5. เกณฑ์การยกระดับความเร่งด่วน (Escalation)", s_h1))

esc_h = [[Paragraph("สถานการณ์", s_th), Paragraph("การดำเนินการ", s_th)]]
esc_r = [
    ["งาน D2 ที่ยังไม่เสร็จใน 4 ชั่วโมง", "ยกระดับเป็น D1 และรายงานหัวหน้าทันที"],
    ["ต้องส่งซ่อมภายนอก", "แจ้งหัวหน้าและติดต่อบริษัทภายในวันนั้น"],
    ["ไม่มีเครื่องสำรอง + งาน D2", "ยกระดับเป็น D1 ทันที"],
    ["งาน D3 ค้างเกิน 3 วันทำการ", "ยกระดับเป็น D2"],
]
esc_data = esc_h + [[Paragraph(a, s_td_l), Paragraph(b, s_td_l)] for a, b in esc_r]
esc_t = Table(esc_data, colWidths=[80*mm, W - 40*mm - 80*mm])
esc_t.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), DARK_BLUE),
    ("BACKGROUND",   (0,1), (-1,-1), LGRAY),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LGRAY]),
    ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
    ("TOPPADDING",   (0,0), (-1,-1), 4),
    ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ("LEFTPADDING",  (0,0), (-1,-1), 5),
]))
story.append(esc_t)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — MORNING CHECKLIST FORM
# ══════════════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 3*mm))
story.append(HRFlowable(width="100%", thickness=2, color=DARK_BLUE))
story.append(Paragraph("6. แบบฟอร์มสรุปงานตอนเช้า — Morning Checklist Summary  (ME-F-01)", s_h1))

form_data = [
    [Paragraph("วันที่", s_bold), Paragraph("...... / ...... / ..........", s_body),
     Paragraph("เวลา", s_bold), Paragraph("......... น.", s_body)],
    [Paragraph("ผู้ปฏิบัติงาน", s_bold), Paragraph("_______________________________", s_body),
     Paragraph("ลงชื่อ", s_bold), Paragraph("_______________________________", s_body)],
]
form_t = Table(form_data, colWidths=[28*mm, 65*mm, 20*mm, 57*mm])
form_t.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (0,-1), LIGHT_BLUE),
    ("BACKGROUND",   (2,0), (2,-1), LIGHT_BLUE),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#BDC3C7")),
    ("TOPPADDING",   (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ("LEFTPADDING",  (0,0), (-1,-1), 4),
]))
story.append(form_t)
story.append(Spacer(1, 2*mm))

sum_header = [[
    Paragraph("ระดับ", s_th), Paragraph("จำนวน (รายการ)", s_th),
    Paragraph("เสร็จแล้ว", s_th), Paragraph("ค้าง", s_th), Paragraph("หมายเหตุ", s_th)
]]
sum_rows = [
    [Paragraph("D1 วิกฤต", style(size=9, color=WHITE, bold=True, align=TA_CENTER)), "", "", "", ""],
    [Paragraph("D2 เร่งด่วน", s_td), "", "", "", ""],
    [Paragraph("D3 ปกติ", s_td), "", "", "", ""],
    [Paragraph("PM", s_td), "", "", "", ""],
    [Paragraph("รวมทั้งหมด", s_bold), "", "", "", ""],
]
sum_data = sum_header + sum_rows
sum_t = Table(sum_data, colWidths=[30*mm, 38*mm, 28*mm, 28*mm, W-40*mm-124*mm])
sum_t.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), DARK_BLUE),
    ("BACKGROUND",   (0,1), (-1,1), colors.HexColor("#FADBD8")),
    ("BACKGROUND",   (0,5), (-1,5), LIGHT_BLUE),
    ("FONTNAME",     (0,1), (0,1), "Sarabun-Bold"),
    ("TEXTCOLOR",    (0,1), (0,1), RED),
    ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
    ("TOPPADDING",   (0,0), (-1,-1), 6),
    ("BOTTOMPADDING",(0,0), (-1,-1), 6),
    ("ALIGN",        (0,0), (-1,-1), "CENTER"),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
]))
story.append(sum_t)

# ══════════════════════════════════════════════════════════════════════════════
# WARNING BOX
# ══════════════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 4*mm))
warn_data = [[
    Paragraph(
        "⚠  ข้อควรระวัง: ห้ามใช้เครื่องมือแพทย์ที่ยังซ่อมไม่เสร็จกับผู้ป่วย จนกว่าจะผ่านการทดสอบและติดป้าย พร้อมใช้งาน แล้วเท่านั้น   |   "
        "งาน D1 ทุกรายการต้องรายงานหัวหน้าหน่วยก่อนและหลังดำเนินการ   |   "
        "บันทึกทุกขั้นตอนการซ่อมลงในระบบหรือแบบฟอร์มทุกครั้ง",
        style(size=8, color=RED, align=TA_CENTER))
]]
warn_t = Table(warn_data, colWidths=[W - 40*mm])
warn_t.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#FDEDEC")),
    ("BOX",          (0,0), (-1,-1), 1, RED),
    ("TOPPADDING",   (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ("LEFTPADDING",  (0,0), (-1,-1), 8),
]))
story.append(warn_t)

# ── Footer ───────────────────────────────────────────────────────────────────
story.append(Spacer(1, 5*mm))
foot_data = [[
    Paragraph("จัดทำโดย: หน่วยวิศวกรรมการแพทย์", s_small),
    Paragraph("อ้างอิง: มาตรฐาน HA | ISO 13485 | กระทรวงสาธารณสุข", style(size=8, color=GRAY, align=TA_CENTER)),
    Paragraph("ทบทวนทุก 1 ปี หรือเมื่อมีการเปลี่ยนแปลงนโยบาย", style(size=8, color=GRAY, align=TA_RIGHT)),
]]
foot_t = Table(foot_data, colWidths=[(W-40*mm)/3]*3)
foot_t.setStyle(TableStyle([
    ("TOPPADDING",   (0,0), (-1,-1), 3),
    ("LINEABOVE",    (0,0), (-1,0), 0.5, GRAY),
]))
story.append(foot_t)

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF created: {OUTPUT}")
