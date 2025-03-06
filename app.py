
import cv2
import numpy as np
from PIL import Image, ImageFilter

def apply_filter(image_path, filter_type):
    image = cv2.imread(image_path)
    if filter_type == "grayscale":
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif filter_type == "blur":
        return cv2.GaussianBlur(image, (15, 15), 0)
    elif filter_type == "edges":
        return cv2.Canny(image, 100, 200)
    elif filter_type == "sharpen":
        pil_image = Image.open(image_path)
        return np.array(pil_image.filter(ImageFilter.SHARPEN))
    else:
        return image


from flask import Flask, request, render_template, send_file
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return "No image uploaded", 400
        image = request.files["image"]
        filter_type = request.form.get("filter")
        if not filter_type:
            return "No filter selected", 400

        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        result_path = os.path.join(RESULT_FOLDER, "result_" + image.filename)
        image.save(image_path)

        result_image = apply_filter(image_path, filter_type)
        cv2.imwrite(result_path, result_image)

        return send_file(result_path, mimetype="image/jpeg")

    return render_template("index.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
