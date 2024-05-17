import pytesseract
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import subprocess
import re

# ฟังก์ชันในการเรียกดูและโหลดรูปภาพ
def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        load_image(file_path)

# ฟังก์ชันในการโหลดและแสดงรูปภาพ
def load_image(file_path):
    image = cv2.imread(file_path)

    # ตรวจสอบว่ารูปภาพถูกโหลดเข้ามาได้หรือไม่
    if not image.size == 0:
        # ทำการปรับขนาดภาพให้เหมาะสม
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # ใช้เทคนิค Adaptive Thresholding เพื่อแปลงรูปภาพเป็นภาพไบนารี
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # สร้าง kernel สำหรับการทำการแปรผันทางโมร์โฟโลจิคัล
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        # ทำการขยายพื้นที่ของวัตถุ
        dilate = cv2.dilate(thresh, kernel, iterations=1)

        # ค้นหา Contours
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        # อ่านข้อมูลที่ต้องการจากบัตรประชาชน
        ocr_result = ""
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            if w > 50 and h > 50:  # ตรวจสอบขนาดพื้นที่ของ Contour
                roi = image[y:y + h, x:x + w]
                text = pytesseract.image_to_string(roi, lang='tha')
                ocr_result += text + "\n"

        # แสดงผลลัพธ์
        show_result(ocr_result)
    else:
        print("ไม่สามารถโหลดรูปภาพได้")

# ฟังก์ชันในการแสดงผลลัพธ์โดยใช้ Tkinter
def show_result(result):
    result_window = tk.Toplevel(root)
    result_window.title("OCR Result")

    result_label = tk.Label(result_window, text=result)
    result_label.pack()

# สร้างหน้าต่างหลักของ Tkinter
root = tk.Tk()
root.title("ID Card OCR")

# สร้างปุ่มสำหรับการเรียกดูรูปภาพและทำ OCR
browse_button = tk.Button(root, text="เรียกดูรูปภาพ", command=browse_image)
browse_button.pack()

root.mainloop()
