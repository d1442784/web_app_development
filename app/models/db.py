import sqlite3
import os

# 預設資料庫路徑 (以 app.py 啟動時為基準)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """
    取得 SQLite 資料庫連線，並設定 row_factory 使查詢結果可以像 dict 一樣操作
    """
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # 啟用 foreign key 支持
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    """
    使用 database/schema.sql 初始化資料庫
    """
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found at {schema_path}")
        
    conn = get_db_connection()
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
