# Hệ Thống Giám Sát Điều Phối Bếp Thông Minh

Dự án này là một hệ thống giám sát thông minh cho khu vực điều hành của bếp thương mại, sử dụng các mô hình AI để phát hiện và phân loại các vật phẩm trên video.

## Kiến trúc

Hệ thống được xây dựng theo kiến trúc microservices và triển khai bằng Docker Compose, bao gồm:
* **`detection-service`**: Một API FastAPI sử dụng mô hình YOLO (`yolov11n.pt`) để phát hiện "khay" và "thức ăn".
* **`classification-service`**: Một API FastAPI sử dụng mô hình phân loại ảnh để xác định một khay có chứa thức ăn hay không.
* **`web-interface`**: Một ứng dụng Streamlit đóng vai trò giao diện người dùng, hiển thị video được phân tích và thu thập phản hồi.

## Yêu cầu hệ thống

* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/)

(Trong môi trường Project IDX, Docker đã được cài đặt sẵn).

## Hướng dẫn Cài đặt và Sử dụng

### 1. Clone Repository

```bash
git clone [https://github.com/TEN_CUA_BAN/smart-kitchen-monitoring.git](https://github.com/TEN_CUA_BAN/smart-kitchen-monitoring.git)
cd smart-kitchen-monitoring