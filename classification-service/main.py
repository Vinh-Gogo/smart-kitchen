from fastapi import FastAPI, File, UploadFile
import torch
import torchvision.transforms as transforms
from PIL import Image
import io

app = FastAPI(title="Classification Service")

# Tải mô hình phân loại (ví dụ)
# Chỉnh sửa phần này để phù hợp với mô hình thực tế của bạn
model = torch.load('./models/tray_classifier.pt')
model.eval()
class_names = ['no_food', 'has_food'] # Giả định thứ tự nhãn

# Định nghĩa các bước tiền xử lý ảnh
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

@app.post("/classify/")
async def classify_image(file: UploadFile = File(...)):
    """
    Nhận ảnh một cái khay và phân loại có thức ăn hay không.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0) # Tạo mini-batch
    
    with torch.no_grad():
        output = model(input_batch)

    _, predicted_idx = torch.max(output, 1)
    class_name = class_names[predicted_idx.item()]
    
    return {"classification": class_name}