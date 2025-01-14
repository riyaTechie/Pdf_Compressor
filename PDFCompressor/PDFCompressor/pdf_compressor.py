import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from tkinter import Tk, filedialog


def compress_pdf(input_path, output_path):
    """
    Compress and resize the pages of a single PDF to 1/4th of their original dimensions.

    Args:
        input_path (str): Input PDF file path.
        output_path (str): Path to save the compressed PDF.
    """
    # Temporary storage for processed images
    temp_images = []

    # Open the PDF with PyMuPDF
    pdf_document = fitz.open(input_path)
    for page_number in range(len(pdf_document)):
        # Render the page to an image
        page = pdf_document[page_number]
        pix = page.get_pixmap(dpi=150)  # Render at 150 DPI for quality
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Resize the image to 1/4th of its original size
        new_width = pix.width // 2
        new_height = pix.height // 2
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Save the resized image to a temporary file
        temp_image_path = f"temp_page_{page_number}.jpg"
        resized_img.save(temp_image_path, "JPEG", quality=50)  # Adjust quality for compression
        temp_images.append(temp_image_path)
    
    pdf_document.close()

    # Create a new PDF from the resized images
    writer = PdfWriter()
    for temp_image in temp_images:
        img = Image.open(temp_image)
        img.save(temp_image.replace('.jpg', '.pdf'), "PDF", resolution=100.0)
        img_pdf = PdfReader(temp_image.replace('.jpg', '.pdf'))
        writer.add_page(img_pdf.pages[0])
        img.close()

    # Save the compressed PDF
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    # Clean up temporary files
    for temp_file in temp_images:
        os.remove(temp_file)
        os.remove(temp_file.replace('.jpg', '.pdf'))

    print(f"Compressed PDF saved to: {output_path}")


if __name__ == "__main__":
    # Use tkinter to open a file dialog for selecting multiple PDF files
    root = Tk()
    root.withdraw()  # Hide the root window

    input_files = filedialog.askopenfilenames(
        title="Select PDF files to compress",
        filetypes=[("PDF files", "*.pdf")]
    )

    if input_files:
        for input_pdf in input_files:
            # Generate output file name based on input file name
            base_name = os.path.splitext(os.path.basename(input_pdf))[0]
            output_pdf = f"{base_name}_compressed.pdf"
            compress_pdf(input_pdf, output_pdf)

        print("Compression completed for all selected files.")
    else:
        print("No files selected.")
