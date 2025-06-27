# Sử dụng base image Python
FROM python:3.11-slim

# Cài đặt các gói hệ thống cần thiết cho OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép tệp requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của service
COPY . .

# Mở cổng cho Streamlit
EXPOSE 8501

# Chạy ứng dụng
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]