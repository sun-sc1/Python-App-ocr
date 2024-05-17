import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import subprocess
import sys
import cv2
import pytesseract

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        load_image(file_path)

def load_image(file_path):
    image = cv2.imread(file_path)
    if image is None:
        print("Error: Unable to read image file.")
        return

    base_image = image.copy()

    # แปลงรูปภาพเป็นโทนส์สีเทา
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ใช้ Gaussian Blur กับรูปภาพ
    blur = cv2.GaussianBlur(gray, (7,7), 0)

    # ใช้การ Thresholding แบบ Otsu's เพื่อค้นหาวัตถุในภาพ (ภาพไบนารี)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # สร้าง kernel สำหรับการทำการแปรผันทางโมร์โฟโลจิคัล
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,25))

    # ทำการขยายพื้นที่ของวัตถุ
    dilate = cv2.dilate(thresh, kernel, iterations=1)

    # ค้นหา Contours
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # เรียง Contours ตามตำแหน่งด้านบน
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])

    # อ่านข้อความจาก Contours และคัดแยกตัวเลขที่สนใจ
    main_text = ""
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if h > 200 and w > 250:  # ตรวจสอบขนาดพื้นที่ของ Contour
            roi = base_image[y:y+h, 0:x]
            constant = cv2.copyMakeBorder(roi.copy(), 30, 30, 30, 30, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            ocr_result = pytesseract.image_to_string(constant)
            
    # อ่านข้อความทั้งหมดจากรูปเพื่อตรวจสอบข้อความที่เกี่ยวข้อง
    ocr_result = pytesseract.image_to_string((base_image), lang='tha+eng')
    print(ocr_result )
    
    # นำข้อความทั้งหมดไปเก็บในไฟล์ text
    with open("result_text.txt", "w",encoding="utf-8") as file:
        file.write(ocr_result + "\n" + main_text)

    # แสดงผลลัพธ์
    show_result(ocr_result)



def show_result(result):
    result_window = tk.Toplevel(root)
    result_window.title("OCR Result")

    result_label = tk.Label(result_window, text=result, font=("Arial", 12))
    result_label.pack(padx=20, pady=20)

    open_button = tk.Button(result_window, text="Open Result Text File", command=open_text_file)
    open_button.pack(pady=10)

    # Center the result window
    result_window.update_idletasks()
    width = result_window.winfo_width()
    height = result_window.winfo_height()
    x = (result_window.winfo_screenwidth() // 2) - (width // 2)
    y = (result_window.winfo_screenheight() // 2) - (height // 2)
    result_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def open_text_file():
    file_path = os.path.join(os.getcwd(), "result_text.txt")
    if os.path.exists(file_path):
        if os.name == 'nt':
            os.startfile(file_path)
        elif os.name == 'posix':
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file_path])

root = tk.Tk()
root.title("Image OCR")

# Styling
root.geometry("400x150")  # Set initial window size

browse_button = tk.Button(root, text="Browse Image", command=browse_image, bg="lightblue", fg="black",
                          font=("Arial", 12))
browse_button.pack(pady=20)

root.mainloop()