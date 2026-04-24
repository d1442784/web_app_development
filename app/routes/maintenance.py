from flask import Blueprint, render_template, request, redirect, url_for

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/garage/<int:v_id>/maintenance/')
def index(v_id):
    """
    GET /garage/<v_id>/maintenance/
    特定車輛的保養紀錄清單
    - 確認車輛存在 (Vehicle.get_by_id)
    - 取得該車的保養紀錄 (MaintenanceRecord.get_by_vehicle)
    - 渲染 maintenance/index.html
    """
    pass

@maintenance_bp.route('/garage/<int:v_id>/maintenance/add', methods=['GET', 'POST'])
def add(v_id):
    """
    GET/POST /garage/<v_id>/maintenance/add
    針對指定車輛新增保養紀錄
    - GET: 渲染 maintenance/form.html
    - POST: 接收表單，呼叫 MaintenanceRecord.create()，重導向至該車的保養清單頁面
    """
    pass

@maintenance_bp.route('/maintenance/<int:m_id>/edit', methods=['GET', 'POST'])
def edit(m_id):
    """
    GET/POST /maintenance/<m_id>/edit
    編輯保養紀錄
    - GET: 取得該紀錄 (MaintenanceRecord.get_by_id)，渲染 maintenance/form.html
    - POST: 接收表單，呼叫 MaintenanceRecord.update()，重導向至該車的保養清單頁面
    """
    pass

@maintenance_bp.route('/maintenance/<int:m_id>/delete', methods=['POST'])
def delete(m_id):
    """
    POST /maintenance/<m_id>/delete
    刪除保養紀錄
    - 取得該紀錄以得知隸屬車輛 ID
    - 呼叫 MaintenanceRecord.delete()
    - 重導向至該車的保養清單頁面
    """
    pass
