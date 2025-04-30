# db_mysql/Dockerfile
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔並安裝套件
COPY db_mysql/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個 db_mysql 進去
COPY db_mysql/ . 

# 執行初始化程式
CMD ["python", "import_data.py"]
