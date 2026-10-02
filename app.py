import streamlit as st
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
import tempfile
import io

st.set_page_config(page_title="PWD Pothole AI Inspector", page_icon="🛣️", layout="wide")

st.title("🛣️ PWD Rajasthan - Automated Pothole AI Inspector")
st.subheader("Video Upload Karein aur Instant Pothole Area ($m^2$) & Excel Report Praapt Karein")

@st.cache_resource
def load_model():
    return YOLO('yolov8n-seg.pt')

model = load_model()

st.sidebar.header("⚙️ Calibration Settings")
pixel_to_meter = st.sidebar.number_input("Pixel to Meter Scale Factor", value=0.0025, format="%.4f")
min_area_filter = st.sidebar.slider("Min Area Filter (sq.m)", 0.01, 0.50, 0.04)

uploaded_video = st.file_uploader("📹 Inspection Video Upload Karein (.mp4, .avi, .mov)", type=["mp4", "avi", "mov"])

if uploaded_video is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())
    
    st.success("✅ Video Successfully Uploaded! Processing shuru ho rahi hai...")
    
    cap = cv2.VideoCapture(tfile.name)
    frame_count = 0
    pothole_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
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
                    pixel_area = cv2.contourArea(cnt)
                    area_sqm = pixel_area * (pixel_to_meter ** 2)
                    
                    if area_sqm >= min_area_filter:
                        rect = cv2.minAreaRect(cnt)
                        (x, y), (w_pix, h_pix), angle = rect
                        length_m = max(w_pix, h_pix) * pixel_to_meter
                        width_m = min(w_pix, h_pix) * pixel_to_meter
                        
                        pothole_data.append({
                            "Frame": frame_count,
                            "Time (Sec)": round(frame_count / 30, 2),
                            "Length (m)": round(length_m, 2),
                            "Width (m)": round(width_m, 2),
                            "Area (sq.m)": round(area_sqm, 3),
                            "Severity": "CRITICAL" if area_sqm > 0.1 else "MODERATE"
                        })
        
        if total_frames > 0:
            progress_bar.progress(min(frame_count / total_frames, 1.0))
            status_text.text(f"Processing Frame {frame_count}/{total_frames}...")

    cap.release()
    status_text.text("✅ Processing Complete!")
    
    df = pd.DataFrame(pothole_data)
    
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Potholes Detected", len(df))
        col2.metric("Total Repair Area (sq.m)", f"{round(df['Area (sq.m)'].sum(), 3)} m²")
        col3.metric("Critical Defects (>0.1 m²)", len(df[df["Severity"] == "CRITICAL"]))
        
        st.subheader("📋 Pothole Inspection Report Table")
        st.dataframe(df, use_container_width=True)
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Pothole_Report')
        
        st.download_button(
            label="📥 Download Excel Report (.xlsx)",
            data=buffer.getvalue(),
            file_name="PWD_Pothole_AI_Inspection_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ Koi Pothole detect nahi hua ya saare minor noise filters se niche hain.")
