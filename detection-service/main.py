from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import io
from PIL import Image

app = FastAPI(title="Detection Service")

# Tải mô hình khi khởi động ứng dụng
model = YOLO('./models/best.pt')

@app.post("/detect/")
async def detect_objects(file: UploadFile = File(...)):
    """
    Nhận file ảnh, thực hiện phát hiện đối tượng và trả về kết quả.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    results = model(image)
    
    detections = []
    for result in results:
        boxes = result.boxes.cpu().numpy()
        for box in boxes:
            detections.append({
                "class_id": int(box.cls[0]),
                "class_name": model.names[int(box.cls[0])],
                "confidence": float(box.conf[0]),
                "box": box.xyxy[0].tolist() # [x1, y1, x2, y2]
            })
            
    return {"detections": detections}