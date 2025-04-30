from db_mysql.connect_database import MySQLConnect

class ViewData:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        db = MySQLConnect()
        db.connect()
        self.conn = db.conn
        self.cursor = db.cursor

    def close(self):
        self.cursor.close()
        self.conn.close()

    def fetch_table(self, table_name: str = 'train', limit: int = 20):
        self.connect()
        self.cursor.execute(f'SELECT * FROM `{table_name}` LIMIT {limit};')
        rows = self.cursor.fetchall()
        return rows

   
