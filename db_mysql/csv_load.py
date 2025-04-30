import os
import pandas as pd
from typing import List, Tuple

class CSVLoad:
    def __init__(self, folder: str = "titanic_file"):
        #os.getcwd()回傳目前當下的工作目錄的完整絕對路徑
        self.folder = os.path.join(os.getcwd(), folder)

    def find_csv_files(self) -> List[str]:
        files = []
        for root, _, filenames in os.walk(self.folder):
            for filename in filenames:
                if filename.startswith(".") or not filename.lower().endswith(".csv"):
                    continue
                files.append(os.path.join(root, filename))
        return files

    def load_csv(self, filepath: str) -> pd.DataFrame:
        df = pd.read_csv(filepath)
        df = df.loc[:, df.columns.notna()]
        df = df.loc[:, df.columns.str.strip() != ""]
        df.columns = df.columns.map(str).str.strip()
        df = df.where(pd.notnull(df), None)
        return df

    def load_all_csv(self) -> List[Tuple[str, pd.DataFrame]]:
        all_data = []
        for filepath in self.find_csv_files():
            #os.path.basename(filepath)-> "test.csv"
            #os.path.splitext(filename)-> "test" , ".csv"
            table_name = os.path.splitext(os.path.basename(filepath))[0]
            df = self.load_csv(filepath)
            all_data.append((table_name, df))
        return all_data
