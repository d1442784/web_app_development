from app.models.db import get_db_connection
from datetime import datetime

class WishlistItem:
    @staticmethod
    def get_by_vehicle(vehicle_id):
        conn = get_db_connection()
        cursor = conn.execute(
            'SELECT * FROM wishlist_items WHERE vehicle_id = ? ORDER BY is_installed ASC, created_at DESC',
            (vehicle_id,)
        )
        items = cursor.fetchall()
        conn.close()
        return [dict(i) for i in items]

    @staticmethod
    def get_by_id(item_id):
        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM wishlist_items WHERE id = ?', (item_id,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    @staticmethod
    def create(vehicle_id, item_name, estimated_cost):
        conn = get_db_connection()
        now = datetime.now().isoformat()
        cursor = conn.execute(
            '''
            INSERT INTO wishlist_items 
            (vehicle_id, item_name, estimated_cost, is_installed, created_at, updated_at)
            VALUES (?, ?, ?, 0, ?, ?)
            ''',
            (vehicle_id, item_name, estimated_cost, now, now)
        )
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()
        return item_id

    @staticmethod
    def update(item_id, item_name, estimated_cost, is_installed):
        conn = get_db_connection()
        updated_at = datetime.now().isoformat()
        conn.execute(
            '''
            UPDATE wishlist_items 
            SET item_name = ?, estimated_cost = ?, is_installed = ?, updated_at = ?
            WHERE id = ?
            ''',
            (item_name, estimated_cost, is_installed, updated_at, item_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def toggle_status(item_id, is_installed):
        """
        快速切換安裝狀態
        """
        conn = get_db_connection()
        updated_at = datetime.now().isoformat()
        conn.execute(
            'UPDATE wishlist_items SET is_installed = ?, updated_at = ? WHERE id = ?',
            (is_installed, updated_at, item_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(item_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM wishlist_items WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
