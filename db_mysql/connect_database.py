import os
import time
import mysql.connector
from mysql.connector import Error
from loguru import logger
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))#載入.env資料庫連線資料檔
class MySQLConnect:
    def __init__(self, max_retries: int = 10, retry_interval: int = 3):
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = int(os.getenv("MYSQL_PORT", 3306))
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "")
        self.database = os.getenv("MYSQL_DATABASE", "titanic")
        self.conn = None
        self.cursor = None
        self.max_retries = max_retries
        self.retry_interval = retry_interval

    def connect(self):
        for i in range(1, self.max_retries + 1):
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )
                self.cursor = self.conn.cursor(dictionary=True)
                logger.success(f"connect success")
                return
            except Error as e:
                logger.warning(f" Try {i} error :{e}")
                time.sleep(self.retry_interval)
        # 如果全部重試失敗
        raise ConnectionError(f"can not connect database")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    def execute(self, sql: str):
        self.cursor.execute(sql)
    def commit(self):
        self.conn.commit()

