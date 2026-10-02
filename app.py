import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO

# 1. Segmentation Model Load Karein
model = YOLO('yolov8n-seg.pt')
video_path = "/content/mixkit-potholes-in-a-rural-road-25208-hd-ready.mp4"

# Calibration Factor (1 pixel = 0.0025 meters approx)
PIXEL_TO_METER = 0.0025

cap = cv2.VideoCapture(video_path)
frame_count = 0
pothole_detailed_report = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    results = model(frame, verbose=False)

    for r in results:
        if r.masks is not None:
            for mask in r.masks.xy:
                cnt = np.array(mask, dtype=np.int32)

                # Area Calculation
                pixel_area = cv2.contourArea(cnt)
                area_sqm = pixel_area * (PIXEL_TO_METER ** 2)

                if area_sqm > 0.04: # Filter noise
                    # Length aur Width Calculation
                    rect = cv2.minAreaRect(cnt)
                    (x, y), (w_pix, h_pix), angle = rect

                    length_m = max(w_pix, h_pix) * PIXEL_TO_METER
                    width_m = min(w_pix, h_pix) * PIXEL_TO_METER

                    pothole_detailed_report.append({
                        "Frame": frame_count,
                        "Time_Sec": round(frame_count / 30, 2),
                        "Length_m": round(length_m, 2),
                        "Width_m": round(width_m, 2),
                        "Area_sqm": round(area_sqm, 3),
                        "Severity": "CRITICAL" if area_sqm > 0.1 else "MODERATE"
                    })

cap.release()

# EXCEL REPORT GENERATION
df_details = pd.DataFrame(pothole_detailed_report)
excel_filename = "Pothole_Size_and_Area_Report.xlsx"
df_details.to_excel(excel_filename, index=False)

print("\n=========================================================================")
print(f"✅ DETAILED REPORT GENERATED: {excel_filename}")
print("=========================================================================")
if not df_details.empty:
    print(df_details.head(10).to_string(index=False))
