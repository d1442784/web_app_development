from app.models.db import get_db_connection
from datetime import datetime

class MaintenanceRecord:
    @staticmethod
    def get_by_vehicle(vehicle_id):
        conn = get_db_connection()
        cursor = conn.execute(
            'SELECT * FROM maintenance_records WHERE vehicle_id = ? ORDER BY service_date DESC, created_at DESC', 
            (vehicle_id,)
        )
        records = cursor.fetchall()
        conn.close()
        return [dict(r) for r in records]

    @staticmethod
    def get_by_id(record_id):
        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM maintenance_records WHERE id = ?', (record_id,))
        record = cursor.fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def create(vehicle_id, item_name, mileage_at_service, interval_mileage, cost, service_date, notes=""):
        conn = get_db_connection()
        created_at = datetime.now().isoformat()
        cursor = conn.execute(
            '''
            INSERT INTO maintenance_records 
            (vehicle_id, item_name, mileage_at_service, interval_mileage, cost, service_date, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (vehicle_id, item_name, mileage_at_service, interval_mileage, cost, service_date, notes, created_at)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    @staticmethod
    def update(record_id, item_name, mileage_at_service, interval_mileage, cost, service_date, notes):
        conn = get_db_connection()
        conn.execute(
            '''
            UPDATE maintenance_records 
            SET item_name = ?, mileage_at_service = ?, interval_mileage = ?, cost = ?, service_date = ?, notes = ?
            WHERE id = ?
            ''',
            (item_name, mileage_at_service, interval_mileage, cost, service_date, notes, record_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM maintenance_records WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_due_maintenance(vehicle_id, current_mileage):
        """
        取得特定車輛即將到期或已到期的保養項目
        回傳每個項目的最後一次保養紀錄，並計算是否到期。
        (假設里程差超過 interval_mileage 即為到期)
        """
        conn = get_db_connection()
        # 利用 GROUP BY 取得各項目最新的保養紀錄
        cursor = conn.execute(
            '''
            SELECT item_name, MAX(mileage_at_service) as last_service_mileage, interval_mileage
            FROM maintenance_records
            WHERE vehicle_id = ? AND interval_mileage IS NOT NULL AND interval_mileage > 0
            GROUP BY item_name
            ''',
            (vehicle_id,)
        )
        latest_records = cursor.fetchall()
        conn.close()

        due_items = []
        for row in latest_records:
            last_service = row['last_service_mileage']
            interval = row['interval_mileage']
            item_name = row['item_name']
            
            # 若目前里程 >= 上次保養里程 + 週期，則為到期
            if current_mileage >= (last_service + interval):
                due_items.append({
                    'item_name': item_name,
                    'last_service_mileage': last_service,
                    'interval_mileage': interval,
                    'due_at_mileage': last_service + interval,
                    'overdue_by': current_mileage - (last_service + interval)
                })

        return due_items
