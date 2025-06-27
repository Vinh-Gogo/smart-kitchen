import streamlit as st
import cv2
import requests
import numpy as np
from PIL import Image
import io
import time
import os

st.set_page_config(layout="wide", page_title="Hệ Thống Giám Sát Bếp")

# URL của các service (Docker Compose sẽ quản lý hostname)
DETECTION_SERVICE_URL = "http://detection-service:8000/detect/"
CLASSIFICATION_SERVICE_URL = "http://classification-service:8000/classify/"
FEEDBACK_PATH = "/app/data/feedback/" # Đường dẫn bên trong container

st.title("Hệ Thống Giám Sát Điều Phối Bếp Thông Minh")

# Tạo thư mục feedback nếu chưa có
os.makedirs(os.path.join(FEEDBACK_PATH, "has_food"), exist_ok=True)
os.makedirs(os.path.join(FEEDBACK_PATH, "no_food"), exist_ok=True)

uploaded_file = st.file_uploader("Tải lên video của bạn", type=['mp4'])
FRAME_WINDOW = st.image([])

if uploaded_file is not None:
    # Lưu file tạm để OpenCV có thể đọc
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    cap = cv2.VideoCapture("temp_video.mp4")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("Kết thúc video.")
            break

        # Chuyển frame sang định dạng ảnh để gửi đi
        _, image_encoded = cv2.imencode(".jpg", frame)
        image_bytes = image_encoded.tobytes()

        # Gọi detection service
        try:
            response_detect = requests.post(DETECTION_SERVICE_URL, files={'file': ('image.jpg', image_bytes, 'image/jpeg')})
            if response_detect.status_code == 200:
                results = response_detect.json()
                
                # Vẽ bounding box và xử lý từng object
                for detection in results.get('detections', []):
                    box = [int(coord) for coord in detection['box']]
                    label = detection['class_name']
                    confidence = detection['confidence']
                    x1, y1, x2, y2 = box
                    
                    # Mặc định màu xanh lá
                    color = (0, 255, 0) 
                    
                    # Nếu là khay, gọi classification service
                    if label == 'khay':
                        tray_img = frame[y1:y2, x1:x2]
                        _, tray_encoded = cv2.imencode(".jpg", tray_img)
                        tray_bytes = tray_encoded.tobytes()
                        
                        try:
                            response_classify = requests.post(CLASSIFICATION_SERVICE_URL, files={'file': ('tray.jpg', tray_bytes, 'image/jpeg')})
                            if response_classify.status_code == 200:
                                classification_result = response_classify.json()['classification']
                                label = f"Khay ({classification_result})"
                                if classification_result == 'no_food':
                                    color = (0, 0, 255) # Màu đỏ cho khay không có thức ăn
                        except requests.exceptions.ConnectionError:
                           label = "Khay (Lỗi phân loại)"
                           color = (0, 255, 255) # Màu vàng
                    
                    # Vẽ lên frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            else:
                st.error(f"Lỗi từ detection service: {response_detect.status_code}")

        except requests.exceptions.ConnectionError as e:
            st.error(f"Không thể kết nối đến detection service: {e}")
            time.sleep(2)


        # Hiển thị frame đã xử lý
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame_rgb)
        
        # Thêm các cột cho chức năng feedback (ví dụ)
        # Chức năng này cần được làm phức tạp hơn để xử lý đúng hình ảnh sai
        # Ví dụ đơn giản:
    
    st.success("Xử lý hoàn tất!")
    st.subheader("Chức năng Feedback (Demo)")
    st.write("Để triển khai chức năng feedback thực tế, bạn cần tạm dừng video, chọn bounding box sai và gửi phản hồi. Hình ảnh và nhãn đúng sẽ được lưu vào thư mục `data/feedback`.")
    
    
    cap.release()