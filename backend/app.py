from flask import Flask, request, jsonify
import os
import requests
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "uploads"
DEST_FOLDER = "resized"
PDF_FILE = "resized_images.pdf"
TARGET_WIDTH = 800
TARGET_HEIGHT = 600
IMGUR_CLIENT_ID = "b359a6736ccbf0b"  # Replace with your Imgur Client ID

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DEST_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "Image Resizer Backend is Running!"})


def upload_to_imgur(file_path):
    url = "https://api.imgur.com/3/upload"
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    with open(file_path, "rb") as file:
        data = {"image": file.read()}
        response = requests.post(url, headers=headers, files={"image": file})
    
    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        raise Exception(f"Imgur upload failed: {response.json()}")


@app.route("/resize", methods=["POST"])
def resize_images():
    uploaded_files = request.files.getlist("images")
    if not uploaded_files:
        return jsonify({"error": "No files provided"}), 400

    report = []
    pdf = canvas.Canvas(PDF_FILE, pagesize=letter)
    pdf.setTitle("Resized Images")

    for uploaded_file in uploaded_files:
        try:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            resized_path = os.path.join(DEST_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            # Resize the image
            with Image.open(file_path) as img:
                img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
                img.save(resized_path)

            # Upload resized image to Imgur
            imgur_url = upload_to_imgur(resized_path)

            # Add resized image to PDF
            pdf.drawImage(resized_path, 50, 500, width=400, height=300)
            pdf.showPage()

            report.append({"file": uploaded_file.filename, "status": "resized", "imgur_url": imgur_url})
        except Exception as e:
            report.append({"file": uploaded_file.filename, "status": f"error: {str(e)}"})

    pdf.save()
    return jsonify({"message": "Resizing complete", "report": report})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

