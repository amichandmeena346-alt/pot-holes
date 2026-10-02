import cv2
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Yahan aapka original Pothole Detection / Processing logic
# ... (YOLO model loading, bounding boxes, length/width/area calculations)

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=5000, debug=True)
