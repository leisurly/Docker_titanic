import os
import pandas as pd
from typing import Dict
from loguru import logger
from connect_database import MySQLConnect
from csv_load import CSVLoad

class DatabaseInit:
    def __init__(self):
        self.db = MySQLConnect()
        self.csv_load = CSVLoad(folder="titanic_file")  


    def create_tables_from_csv(self):
        self.db.connect()
        csv_table = self.csv_load.load_all_csv()
        for table_name, df in csv_table:
            create_sql = self.create_sql_column(table_name, df)
            logger.debug(f"excute SQL:\n{create_sql.strip()}")
            self.db.execute(create_sql)
            self.db.commit()
        self.db.close()

    @staticmethod #讓這個方法不會自動傳入self 放在 class 裡做分類管理
    def create_sql_column(table_name: str, df: pd.DataFrame) -> str:
        type_mapping: Dict[str, str] = {
            "object": "VARCHAR(150)",
            "int64": "INT",
            "float64": "FLOAT",
            "bool": "BOOLEAN",
            "datetime64[ns]": "DATETIME"
        }

        columns = []
        primary_key = None
        clean_columns = [col for col in df.columns if pd.notna(col) and str(col).strip() != ""]

        for col_name in clean_columns:
            dtype = df[col_name].dtype
            sql_type = type_mapping.get(str(dtype), "VARCHAR(150)")

            if primary_key is None and "id" in col_name.lower() and str(dtype) == "int64":
                primary_key = col_name
            # 、、 格式化字串
            columns.append(f"`{col_name}` {sql_type}")

        columns_sql = ",\n  ".join(columns)

        if primary_key:
            return f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` (
              {columns_sql},
              PRIMARY KEY (`{primary_key}`)
            );
            """
        else:
            return f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` (
              {columns_sql}
            );
            """
        
if __name__ == "__main__":
    db_init = DatabaseInit()
    db_init.create_tables_from_csv()
