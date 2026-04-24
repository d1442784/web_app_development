from app.models.db import get_db_connection
from datetime import datetime

class Vehicle:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM vehicles ORDER BY created_at DESC')
        vehicles = cursor.fetchall()
        conn.close()
        return [dict(v) for v in vehicles]

    @staticmethod
    def get_by_id(vehicle_id):
        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM vehicles WHERE id = ?', (vehicle_id,))
        vehicle = cursor.fetchone()
        conn.close()
        return dict(vehicle) if vehicle else None

    @staticmethod
    def create(brand, model_name, current_mileage):
        conn = get_db_connection()
        created_at = datetime.now().isoformat()
        cursor = conn.execute(
            'INSERT INTO vehicles (brand, model_name, current_mileage, created_at) VALUES (?, ?, ?, ?)',
            (brand, model_name, current_mileage, created_at)
        )
        conn.commit()
        vehicle_id = cursor.lastrowid
        conn.close()
        return vehicle_id

    @staticmethod
    def update(vehicle_id, brand, model_name, current_mileage):
        conn = get_db_connection()
        conn.execute(
            'UPDATE vehicles SET brand = ?, model_name = ?, current_mileage = ? WHERE id = ?',
            (brand, model_name, current_mileage, vehicle_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(vehicle_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM vehicles WHERE id = ?', (vehicle_id,))
        conn.commit()
        conn.close()
