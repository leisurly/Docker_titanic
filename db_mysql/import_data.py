import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from typing import List, Tuple
from loguru import logger
from connect_database import MySQLConnect
from set_database import DatabaseInit
from csv_load import CSVLoad 

class ImportData:
    def __init__(self, folder: str = "titanic_file", batch_size: int = 100):
        self.conn = None
        self.cursor = None
        self.load = CSVLoad(folder)
        self.batch_size = batch_size
        self.inserted = 0
        self.failed = 0

    def connect(self):
        db = MySQLConnect()
        db.connect()
        self.conn = db.conn
        self.cursor = db.cursor

    def close(self):
        self.cursor.close()
        self.conn.close()

    def import_all(self):
        self.connect()
        csv_files = self.load.find_csv_files()  
        for filepath in tqdm(csv_files, desc="process.."):
            try:
                df = self.load.load_csv(filepath)
                if df.empty:
                    logger.warning(f"{filepath} is emypt")
                    continue

                table_name = os.path.splitext(os.path.basename(filepath))[0]
                insert_sql, clean_columns = self.clean_data(table_name, df)
                batch = []
                #全部的row[name] row[age] 產生一個tuple series
                for _, row in df.iterrows():
                    data = tuple(
                        None if pd.isna(item) else
                        int(item) if isinstance(item, np.integer) else
                        float(item) if isinstance(item, np.floating) else
                        item
                        for item in (row[col] for col in clean_columns)
                    )
                    batch.append(data)
                    if len(batch) >= self.batch_size:
                        #cursor.executemany() 批次執行方法
                        self.cursor.executemany(insert_sql, batch)
                        self.conn.commit()
                        self.inserted += len(batch)
                        batch = []
                if batch:
                    self.cursor.executemany(insert_sql, batch)
                    self.conn.commit()
                    self.inserted += len(batch)
            except Exception as e:
                logger.error(f"{filepath} import false: {e}")
                self.failed += 1
        self.close()
        logger.success(f"import sucess: {self.inserted} import false: {self.failed} ")


    def clean_data(self, table_name: str, df: pd.DataFrame) -> Tuple[str, List[str]]:
        clean_columns = [col for col in df.columns if pd.notna(col) and str(col).strip() != ""]
        placeholders = ", ".join(["%s"] * len(clean_columns))
        columns = ", ".join([f"`{col}`" for col in clean_columns])
        sql = f"INSERT IGNORE INTO `{table_name}` ({columns}) VALUES ({placeholders})"
        return sql, clean_columns


if __name__ == "__main__":
    db_init = DatabaseInit()
    db_init.create_tables_from_csv()
    import_data = ImportData()
    import_data.import_all()
