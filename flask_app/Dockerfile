# flask_app/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安裝 flask_app 中的 requirements.txt
COPY flask_app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY flask_app/ .

# 設定 PYTHONPATH 允許跨資料夾 import
ENV PYTHONPATH=/app
# 進入 flask_app 執行主程式
CMD ["python", "flask_app.py"]
