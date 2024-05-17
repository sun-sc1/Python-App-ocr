from tkinter import Tk, Canvas, Button, PhotoImage, filedialog
from pathlib import Path
from PIL import Image, ImageTk
import pytesseract
import re

def extract_text(image_path):

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)
    return text

def display_text_on_canvas(tax_id, par_id, canvas):

    canvas.delete("text") 
  
    canvas.create_text(50, 180, anchor="nw", text=f"TAX ID: {tax_id}", font=("Arial", 14), fill="black", tag="text") #tax_id
    canvas.create_text(50, 230, anchor="nw", text=f"Parking Fee: {par_id}", font=("Arial", 14), fill="black", tag="text") #par_id

def browse_image_and_extract_text(canvas):
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
 
        extracted_text = extract_text(image_path)
     
        tax_id_match = re.search(r'TAX ID: (\d+)', extracted_text)
        if tax_id_match:
            tax_id = tax_id_match.group(1)
      
            par_id_match = re.search(r'Parking Fee: (\d+)', extracted_text)
            if par_id_match:
                par_id = par_id_match.group(1)
                display_text_on_canvas(tax_id, par_id, canvas)
            else:
                display_text_on_canvas(tax_id, "Parking Fee not found", canvas)
        else:
            display_text_on_canvas("TAX ID not found", "", canvas)


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\warin\OneDrive\เดสก์ท็อป\pyocr_fixed\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("330x400")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=400,
    width=330,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(165.0, 34.0, image=image_image_1)


canvas.create_rectangle(
    100.0,
    150.0,
    310.0,
    400.0, 
    fill="#FFFFFF",
    outline=""
)


button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
browse_button = Button(
    window,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: browse_image_and_extract_text(canvas),
    relief="flat"
)
browse_button.place(
    x=95.0,
    y=339.0,
    width=139.1999969482422,
    height=31.36480712890625
)

canvas.create_rectangle(
    150.0,
    300.0,
    267.0,
    319.0,
    fill="#FFFFFF",
    outline=""
)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(78.0, 34.0, image=image_image_2)

window.title('OCR Receipt')
window.wm_attributes('-toolwindow', True)
window.resizable(False, False)

window.mainloop()