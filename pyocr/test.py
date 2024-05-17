import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import sys
import pytesseract
from PIL import Image

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        ocr_result = perform_ocr(file_path)
        show_result(ocr_result)

def perform_ocr(file_path):
    ocr_result = pytesseract.image_to_string(Image.open(file_path))
    return ocr_result

def show_result(result):
    result_window = tk.Toplevel(root)
    result_window.title("OCR Result")
    result_label = tk.Label(result_window, text=result, font=("Arial", 12))
    result_label.pack(padx=20, pady=20)

    open_button = tk.Button(result_window, text="Open Result Text File", command=lambda: open_text_file(result))
    open_button.pack(pady=10)

    # Center the result window
    result_window.update_idletasks()
    width = result_window.winfo_width()
    height = result_window.winfo_height()
    x = (result_window.winfo_screenwidth() // 2) - (width // 2)
    y = (result_window.winfo_screenheight() // 2) - (height // 2)
    result_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def open_text_file(result):
    with open("result_text.txt", "w") as file:
        file.write(result)

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

browse_button = tk.Button(root, text="Browse Image", command=browse_image, bg="lightblue", fg="black", font=("Arial", 12))
browse_button.pack(pady=20)

root.mainloop()
