# Sử dụng base image Python
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép tệp requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của service
COPY . .

# Chạy ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]