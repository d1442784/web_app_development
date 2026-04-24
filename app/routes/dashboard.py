from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """
    GET /
    首頁儀表板
    - 取得所有車輛 (Vehicle.get_all)
    - 針對每台車輛，檢查是否有即將到期的保養項目 (MaintenanceRecord.get_due_maintenance)
    - 渲染 dashboard/index.html
    """
    pass
