# Sử dụng một base image Python chính thức
FROM python:3.11-slim-buster
# Hoặc python:3.10-slim-buster, python:3.11-slim-buster tùy phiên bản bạn dùng

# Thiết lập các biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Đặt biến này nếu bạn muốn, hoặc đặt khi chạy container. 
# Thay 'your_project_name' bằng tên thư mục project của bạn (nơi chứa settings.py)
ENV DJANGO_SETTINGS_MODULE english_web.settings 

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt các dependencies hệ thống (nếu cần, ví dụ: cho psycopg2 hoặc Pillow)
# Bỏ comment và thêm các thư viện cần thiết nếu có
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # ví dụ cho postgresql:
    libpq-dev \
    gcc \
    # ví dụ cho pillow:
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    libtiff5-dev \
    libopenjp2-7-dev \
    && rm -rf /var/lib/apt/lists/*

# Sao chép file requirements vào trước để tận dụng Docker layer caching
COPY requirements.txt .

# Cài đặt các Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Sao chép toàn bộ mã nguồn của dự án vào thư mục làm việc
# Đảm bảo bạn có file .dockerignore để loại trừ các file/thư mục không cần thiết
COPY . .

# Thu thập static files (nếu bạn dùng Django để phục vụ static files với Whitenoise)
# Nếu bạn dùng Nginx hoặc CDN riêng cho static files, bạn có thể không cần bước này ở đây.
# Đảm bảo STATIC_ROOT được cấu hình trong settings.py
RUN python manage.py collectstatic --noinput --clear

# Expose cổng mà Gunicorn sẽ chạy trên đó (ví dụ: 8000)
EXPOSE 8000

# Lệnh để chạy ứng dụng khi container khởi động
# Thay 'your_project_name.wsgi:application' bằng đường dẫn đúng đến file wsgi.py của bạn
# Ví dụ: nếu thư mục project chính (chứa settings.py, wsgi.py) của bạn tên là 'core_project',
# thì sẽ là 'core_project.wsgi:application'
# Nếu nó nằm ngay trong thư mục gốc cùng manage.py và tên thư mục project là 'myproject',
# thì có thể là 'myproject.wsgi:application'
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "english_web.wsgi:application"]