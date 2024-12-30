import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Configuration
source_folder = r"F:\image-resizer\backend\uploads"
destination_folder = r"F:\image-resizer\backend\resized"
report_file = os.path.join(destination_folder, "resize_report.txt")
pdf_file = os.path.join(destination_folder, "resized_images.pdf")
target_width = 800  # Desired width in pixels
target_height = 600  # Desired height in pixels

# Ensure destination folder exists
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Open report file
with open(report_file, "w") as report:
    report.write("Resize Report\n")
    report.write("=======================\n")

    def resize_image(file_path, save_path, width, height):
        try:
            with Image.open(file_path) as img:
                # Resize image while maintaining aspect ratio
                img = img.resize((width, height), Image.LANCZOS)
                img.save(save_path)
                print(f"Source: {file_path}, Resized: {save_path}")
                report.write(f"Source: {file_path}, Resized: {save_path}\n")
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")
            report.write(f"Failed to process {file_path}: {e}\n")

    # Create PDF
    pdf = canvas.Canvas(pdf_file, pagesize=letter)
    pdf.setTitle("Resized Images")

    # Process all images in the source folder
    for file_name in os.listdir(source_folder):
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)

        # Check if the file is an image
        if os.path.isfile(source_path):
            try:
                resize_image(source_path, destination_path, target_width, target_height)

                # Add resized image to the PDF
                pdf.drawImage(destination_path, 50, 500, width=400, height=300)  # Adjust position and size as needed
                pdf.showPage()
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                report.write(f"Error processing {file_name}: {e}\n")

    pdf.save()
    print(f"PDF saved to {pdf_file}")
    report.write(f"PDF saved to {pdf_file}\n")

    print("All images processed successfully.")
    report.write("All images processed successfully.\n")
