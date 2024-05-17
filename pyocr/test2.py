import cv2
import pytesseract
import time
import tkinter as tk
from tkinter import filedialog
import sys

# Function to browse and select image
def browse_image():
    """Opens a file dialog and returns the selected image path."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])  # Ask the user to select a file
    return file_path

# Load PyTesseract library (assuming Tesseract is installed in the default location)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def main():
    """Main function for reading QR code."""
    # Start timing
    start = time.time()

    # Read image using browse_image function
    file_path = browse_image()
    if not file_path:
        print("No image selected. Exiting...")
        sys.exit()  # Exit the program

    img = cv2.imread(file_path)

    # Check if image is read successfully
    if img is None:
        print("Error reading image. Please check the file path.")
        sys.exit()  # Exit the program

    # Resize image to 600x400 (as per your request)
    img = cv2.resize(img, (600, 400))

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding to create a binary image
    _, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Show image for selecting the area to read
    cv2.imshow("Select OCR area to Read", img)
    r = cv2.selectROI("Select OCR area to Read", img)
    cv2.destroyWindow("Select OCR area to Read")

    # Crop the image
    cropped_image = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

    # Additional image processing (if needed)
    # For example, you can apply further image processing techniques here
    
    # Read text from the cropped image
    read_from_tess = pytesseract.image_to_string(cropped_image, lang='tha')

    # Display the result
    print("Result:")
    print(read_from_tess.replace("\n", ""))

    # End timing
    end = time.time()
    print("Processing time:", end - start, "seconds")
    print("Pieces/minute:", int(60 / (end - start)))

    # Exit the program
    sys.exit()

# Run the main function
if __name__ == "__main__":
    main()
