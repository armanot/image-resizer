document.addEventListener("DOMContentLoaded", () => {
    const cameraInput = document.getElementById("cameraInput");
    const preview = document.getElementById("preview");
    const resizeButton = document.getElementById("resizeButton");
    const uploadButton = document.getElementById("uploadButton");
    const canvas = document.createElement("canvas");
    let imageFile;
  
    // Capture image from camera input
    cameraInput.addEventListener("change", (event) => {
      const file = event.target.files[0];
      if (file) {
        imageFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          preview.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  
    // Resize image using Canvas
    resizeButton.addEventListener("click", () => {
      if (!imageFile) {
        alert("Please select an image first!");
        return;
      }
      const ctx = canvas.getContext("2d");
      const img = new Image();
      img.onload = () => {
        canvas.width = 800; // Desired width
        canvas.height = 600; // Desired height
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        preview.src = canvas.toDataURL("image/jpeg", 0.9);
        alert("Image resized successfully!");
      };
      img.src = preview.src;
    });
  
    // Upload resized image to the backend
    uploadButton.addEventListener("click", async () => {
      if (!canvas.toDataURL()) {
        alert("Please resize the image first!");
        return;
      }
  
      canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("images", blob, "resized-image.jpg");
  
        try {
          const response = await fetch("https://image-resizer-4x4k.onrender.com/resize", {
            method: "POST",
            body: formData,
          });
  
          if (!response.ok) {
            throw new Error("Failed to upload the image.");
          }
  
          const data = await response.json();
          console.log(data);
          alert("Image uploaded and processed successfully!");
        } catch (error) {
          console.error("Upload failed:", error);
          alert("An error occurred during upload.");
        }
      }, "image/jpeg", 0.9);
    });
  });
  