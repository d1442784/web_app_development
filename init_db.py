import os
import sys

# 確保可以 import app 模組
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.db import init_db

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Database initialized successfully at instance/database.db!")
