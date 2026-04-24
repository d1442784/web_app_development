from flask import Blueprint, render_template, request, redirect, url_for

garage_bp = Blueprint('garage', __name__, url_prefix='/garage')

@garage_bp.route('/')
def index():
    """
    GET /garage/
    車庫列表
    - 取得所有車輛 (Vehicle.get_all)
    - 渲染 garage/index.html
    """
    pass

@garage_bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    GET/POST /garage/add
    新增車輛
    - GET: 渲染 garage/form.html
    - POST: 接收表單，呼叫 Vehicle.create()，重導向至 /garage/
    """
    pass

@garage_bp.route('/<int:v_id>/edit', methods=['GET', 'POST'])
def edit(v_id):
    """
    GET/POST /garage/<v_id>/edit
    編輯車輛
    - GET: 取得特定車輛 (Vehicle.get_by_id)，渲染 garage/form.html
    - POST: 接收表單，呼叫 Vehicle.update()，重導向至 /garage/
    """
    pass

@garage_bp.route('/<int:v_id>/delete', methods=['POST'])
def delete(v_id):
    """
    POST /garage/<v_id>/delete
    刪除車輛
    - 呼叫 Vehicle.delete()
    - 重導向至 /garage/
    """
    pass
